"""
LiteLLM client wrapper with token counting and error handling
"""

import os
from typing import Optional, Dict, Iterator
import config

try:
    import litellm
    from litellm import responses, token_counter, get_max_tokens, validate_environment
    LITELLM_AVAILABLE = True
except ImportError:
    LITELLM_AVAILABLE = False


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
        stream: bool = False,
        **kwargs
    ) -> Iterator[Dict]:
        """Make a request using the responses API (auto-bridges to completion for unsupported models)"""

        response_kwargs = {
            "model": model,
            "input": prompt,
            "stream": stream,
            **kwargs
        }

        if self.base_url:
            response_kwargs["api_base"] = self.base_url

        try:
            response = responses(**response_kwargs)

            if stream:
                for chunk in response:
                    # Handle streaming response format
                    if hasattr(chunk, 'choices') and len(chunk.choices) > 0:
                        choice = chunk.choices[0]
                        # Check for delta content (streaming format)
                        if hasattr(choice, 'delta') and hasattr(choice.delta, 'content'):
                            content = choice.delta.content
                            if content:
                                yield {"content": content}
                        # Check for message content (some models use this)
                        elif hasattr(choice, 'message') and hasattr(choice.message, 'content'):
                            content = choice.message.content
                            if content:
                                yield {"content": content}
            else:
                # Non-streaming response
                if hasattr(response, 'choices') and len(response.choices) > 0:
                    message = response.choices[0].message
                    yield {
                        "content": message.content if hasattr(message, 'content') else str(message),
                        "usage": response.usage if hasattr(response, 'usage') else None
                    }
                else:
                    raise RuntimeError("Invalid response format from LLM")

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
            messages = [{"role": "user", "content": text}]
            return token_counter(model=model, messages=messages)
        except Exception:
            # Fallback: rough estimate (4 chars per token)
            return max(1, len(text) // 4)

    def get_max_tokens(self, model: str) -> int:
        """Get maximum context size for model"""

        try:
            return get_max_tokens(model)
        except Exception:
            # Try known models
            if model in config.KNOWN_CONTEXT_SIZES:
                return config.KNOWN_CONTEXT_SIZES[model]
            # Conservative fallback
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
            result = list(self.complete(
                model=model,
                prompt="Hello",
                max_tokens=5
            ))
            return len(result) > 0
        except Exception:
            return False
