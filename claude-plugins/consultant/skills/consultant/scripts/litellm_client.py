"""
LiteLLM client wrapper with token counting and error handling
"""

import os
from pathlib import Path
from typing import Optional, Dict
import config

try:
    import litellm
    from litellm import responses, token_counter, get_max_tokens, validate_environment
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
            **kwargs: Additional args passed to litellm.responses()

        Returns:
            Dict with 'content' and optional 'usage'
        """

        # Add base_url if configured
        if self.base_url:
            kwargs["api_base"] = self.base_url

        # Select appropriate strategy based on model
        strategy = ResponseStrategyFactory.get_strategy(model)

        if session_dir:
            print(f"Using {strategy.__class__.__name__} (resumable: {strategy.can_resume()})")

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
        """Count tokens for given text and model"""

        try:
            # Use text parameter directly for plain text (not chat messages)
            return token_counter(model=model, text=text)
        except Exception:
            # Fallback: rough estimate (4 chars per token)
            return max(1, len(text) // 4)

    def get_max_tokens(self, model: str) -> int:
        """Get maximum context size for model"""

        try:
            return get_max_tokens(model)
        except Exception:
            # Try get_model_info as fallback
            try:
                info = get_model_info(model=model)
                return info.get("max_tokens", 8192)
            except Exception:
                # Conservative fallback if both methods fail
                return 8192

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
