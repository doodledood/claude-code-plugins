"""
LiteLLM client wrapper with token counting and error handling
"""

import os
import requests
from pathlib import Path
from typing import Optional, Dict
import config

try:
    import litellm
    from litellm import responses, token_counter, get_max_tokens, validate_environment, completion_cost
    from litellm.utils import get_model_info
    LITELLM_AVAILABLE = True
except ImportError:
    LITELLM_AVAILABLE = False

from response_strategy import ResponseStrategyFactory


class LiteLLMClient:
    """Wrapper around LiteLLM with enhanced functionality"""

    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        if not LITELLM_AVAILABLE:
            raise ImportError(
                "LiteLLM is not installed. Install with: pip install litellm"
            )

        self.base_url = base_url
        self.api_key = api_key or config.get_api_key()

        # Configure litellm
        if self.api_key:
            # Set API key in environment for litellm to pick up
            if not os.environ.get("OPENAI_API_KEY"):
                os.environ["OPENAI_API_KEY"] = self.api_key

    def complete(
        self,
        model: str,
        prompt: str,
        session_dir: Optional[Path] = None,
        reasoning_effort: str = "high",
        **kwargs
    ) -> Dict:
        """
        Make a request using the responses API with automatic retry/background job handling.

        Uses strategy pattern to:
        - Use background jobs for OpenAI/Azure (resumable after network failures)
        - Use sync with retries for other providers

        Args:
            model: Model identifier
            prompt: Full prompt text
            session_dir: Optional session directory for state persistence (enables resumability)
            reasoning_effort: Reasoning effort level (low, medium, high) - default high
            **kwargs: Additional args passed to litellm.responses()

        Returns:
            Dict with 'content' and optional 'usage'
        """

        # Add base_url if configured
        if self.base_url:
            kwargs["api_base"] = self.base_url

        # Add reasoning_effort parameter
        kwargs["reasoning_effort"] = reasoning_effort

        # Select appropriate strategy based on model
        strategy = ResponseStrategyFactory.get_strategy(model)

        if session_dir:
            print(f"Using {strategy.__class__.__name__} (resumable: {strategy.can_resume()})")
            print(f"Reasoning effort: {reasoning_effort}")

        try:
            # Execute with strategy-specific retry/background logic
            return strategy.execute(
                model=model,
                prompt=prompt,
                session_dir=session_dir,
                **kwargs
            )

        except Exception as e:
            # Map to standardized errors
            error_msg = str(e)

            if "context" in error_msg.lower() or "token" in error_msg.lower():
                raise ValueError(f"Context limit exceeded: {error_msg}")
            elif "auth" in error_msg.lower() or "key" in error_msg.lower():
                raise PermissionError(f"Authentication failed: {error_msg}")
            elif "not found" in error_msg.lower() or "404" in error_msg:
                raise ValueError(f"Model not found: {error_msg}")
            else:
                raise RuntimeError(f"LLM request failed: {error_msg}")

    def count_tokens(self, text: str, model: str) -> int:
        """
        Count tokens for given text and model.

        When base_url is set (proxy mode), uses the proxy's /utils/token_counter endpoint
        for accurate tokenization of custom models. Otherwise uses local token_counter.
        """

        # If using a proxy (base_url set), use the proxy's token counter endpoint
        if self.base_url:
            url = f"{self.base_url.rstrip('/')}/utils/token_counter"
            payload = {
                "model": model,
                "text": text
            }

            headers = {"Content-Type": "application/json"}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"

            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()

            # Response typically has format: {"token_count": 123}
            result = response.json()
            token_count = result.get("token_count") or result.get("tokens")
            if token_count is None:
                raise RuntimeError(f"Proxy token counter returned invalid response: {result}")
            return token_count

        # Use local token counter (direct API mode)
        return token_counter(model=model, text=text)

    def get_max_tokens(self, model: str) -> int:
        """Get maximum context size for model"""

        try:
            return get_max_tokens(model)
        except Exception as e:
            # Try get_model_info as alternative method
            try:
                info = get_model_info(model=model)
                max_tokens = info.get("max_tokens")
                if max_tokens is None:
                    raise RuntimeError(f"Could not determine max_tokens for model {model}")
                return max_tokens
            except Exception as inner_e:
                raise RuntimeError(f"Could not get max tokens for model {model}: {e}, {inner_e}")

    def calculate_cost(self, model: str, response=None, usage: Optional[Dict] = None) -> Optional[Dict]:
        """
        Calculate cost using LiteLLM's built-in completion_cost() function.

        Args:
            model: Model identifier
            response: Optional response object from litellm.responses()
            usage: Optional usage dict (fallback if response not available)

        Returns:
            Dict with input_tokens, output_tokens, costs, or None if unavailable
        """
        try:
            # Prefer using response object with built-in function
            if response:
                total_cost = completion_cost(completion_response=response)

                # Extract token counts from response.usage if available
                if hasattr(response, 'usage'):
                    usage = response.usage

            # Calculate from usage dict if provided
            if usage:
                input_tokens = usage.get("prompt_tokens") or usage.get("input_tokens", 0)
                output_tokens = usage.get("completion_tokens") or usage.get("output_tokens", 0)

                # Get per-token costs from model info
                info = get_model_info(model=model)
                input_cost_per_token = info.get("input_cost_per_token", 0)
                output_cost_per_token = info.get("output_cost_per_token", 0)

                input_cost = input_tokens * input_cost_per_token
                output_cost = output_tokens * output_cost_per_token

                # Use total_cost from completion_cost if available, else calculate
                if not response:
                    total_cost = input_cost + output_cost

                return {
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "input_cost": input_cost,
                    "output_cost": output_cost,
                    "total_cost": total_cost,
                    "currency": "USD"
                }

            return None

        except Exception:
            # If we can't get pricing info, return None
            return None

    def validate_environment(self, model: str) -> Dict:
        """
        Check if required environment variables are set for the model.
        Returns dict with 'keys_in_environment' (bool) and 'missing_keys' (list).
        """
        try:
            return validate_environment(model=model)
        except Exception as e:
            # If validation fails, return a generic response
            return {
                "keys_in_environment": False,
                "missing_keys": ["API_KEY"],
                "error": str(e)
            }

    def test_connection(self, model: str) -> bool:
        """Test if we can connect to the model"""

        try:
            result = self.complete(
                model=model,
                prompt="Hello",
                max_tokens=5
            )
            return result.get("content") is not None
        except Exception:
            return False
