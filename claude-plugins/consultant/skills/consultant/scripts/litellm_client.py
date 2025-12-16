"""
LiteLLM client wrapper with token counting and error handling
"""

import os
from pathlib import Path
from typing import Any

import requests
from litellm import (
    completion_cost,
    get_max_tokens,
    token_counter,
    validate_environment,
)
from litellm.utils import get_model_info

import config
from response_strategy import ResponseStrategyFactory


class LiteLLMClient:
    """Wrapper around LiteLLM with enhanced functionality"""

    def __init__(self, base_url: str | None = None, api_key: str | None = None) -> None:
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
        session_dir: Path | None = None,
        reasoning_effort: str = "xhigh",
        multimodal_content: list[dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Make a request using the responses API with automatic retry/background job handling.

        Uses strategy pattern to:
        - Use background jobs for OpenAI/Azure (resumable after network failures)
        - Use sync with retries for other providers

        Args:
            model: Model identifier
            prompt: Full prompt text
            session_dir: Optional session directory for state persistence (enables resumability)
            reasoning_effort: Reasoning effort level (low, medium, high, xhigh) - default xhigh
            multimodal_content: Optional multimodal content array for images
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
            api_type = ResponseStrategyFactory.get_api_type(model)
            print(
                f"Using {strategy.__class__.__name__} (resumable: {strategy.can_resume()})"
            )
            print(f"API: {api_type} | Reasoning effort: {reasoning_effort}")

        try:
            # Execute with strategy-specific retry/background logic
            result: dict[str, Any] = strategy.execute(
                model=model,
                prompt=prompt,
                session_dir=session_dir,
                multimodal_content=multimodal_content,
                **kwargs,
            )
            return result

        except Exception as e:
            # Map to standardized errors
            error_msg = str(e)

            if "context" in error_msg.lower() or "token" in error_msg.lower():
                raise ValueError(f"Context limit exceeded: {error_msg}") from e
            elif "auth" in error_msg.lower() or "key" in error_msg.lower():
                raise PermissionError(f"Authentication failed: {error_msg}") from e
            elif "not found" in error_msg.lower() or "404" in error_msg:
                raise ValueError(f"Model not found: {error_msg}") from e
            else:
                raise RuntimeError(f"LLM request failed: {error_msg}") from e

    def count_tokens(self, text: str, model: str) -> int:
        """
        Count tokens for given text and model.

        When base_url is set (proxy mode), uses the proxy's /utils/token_counter endpoint
        for accurate tokenization of custom models. Otherwise uses local token_counter.
        """

        # If using a proxy (base_url set), use the proxy's token counter endpoint
        if self.base_url:
            url = f"{self.base_url.rstrip('/')}/utils/token_counter"
            payload = {"model": model, "text": text}

            headers = {"Content-Type": "application/json"}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"

            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()

            # Response typically has format: {"token_count": 123}
            result = response.json()
            token_count = result.get("token_count") or result.get("tokens")
            if token_count is None:
                raise RuntimeError(
                    f"Proxy token counter returned invalid response: {result}"
                )
            return int(token_count)

        # Use local token counter (direct API mode)
        return int(token_counter(model=model, text=text))

    def get_max_tokens(self, model: str) -> int:
        """Get maximum context size for model"""

        try:
            return int(get_max_tokens(model))
        except Exception as e:
            # Try get_model_info as alternative method
            try:
                info = get_model_info(model=model)
                max_tokens = info.get("max_tokens")
                if max_tokens is None:
                    raise RuntimeError(
                        f"Could not determine max_tokens for model {model}"
                    )
                return int(max_tokens)
            except Exception as inner_e:
                raise RuntimeError(
                    f"Could not get max tokens for model {model}: {e}, {inner_e}"
                ) from inner_e

    def calculate_cost(
        self,
        model: str,
        response: Any = None,
        usage: dict[str, Any] | None = None,
    ) -> dict[str, Any] | None:
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
                if hasattr(response, "usage"):
                    usage = response.usage

            # Calculate from usage dict if provided
            if usage:
                input_tokens = usage.get("prompt_tokens") or usage.get(
                    "input_tokens", 0
                )
                output_tokens = usage.get("completion_tokens") or usage.get(
                    "output_tokens", 0
                )

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
                    "currency": "USD",
                }

            return None

        except Exception:
            # If we can't get pricing info, return None
            return None

    def validate_environment(self, model: str) -> dict[str, Any]:
        """
        Check if required environment variables are set for the model.
        Returns dict with 'keys_in_environment' (bool) and 'missing_keys' (list).
        """
        try:
            result: dict[str, Any] = validate_environment(model=model)
            return result
        except Exception as e:
            # If validation fails, return a generic response
            return {
                "keys_in_environment": False,
                "missing_keys": ["API_KEY"],
                "error": str(e),
            }

    def test_connection(self, model: str) -> bool:
        """Test if we can connect to the model"""

        try:
            result = self.complete(model=model, prompt="Hello", max_tokens=5)
            return result.get("content") is not None
        except Exception:
            return False
