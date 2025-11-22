"""
LiteLLM client wrapper with token counting and error handling
"""

import os
from typing import Optional, Dict, Iterator
import config

try:
    import litellm
    from litellm import completion, token_counter, get_max_tokens
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
        """Make a completion request"""

        messages = [{"role": "user", "content": prompt}]

        completion_kwargs = {
            "model": model,
            "messages": messages,
            "stream": stream,
            **kwargs
        }

        if self.base_url:
            completion_kwargs["api_base"] = self.base_url

        try:
            response = completion(**completion_kwargs)

            if stream:
                for chunk in response:
                    if hasattr(chunk.choices[0], 'delta') and hasattr(chunk.choices[0].delta, 'content'):
                        content = chunk.choices[0].delta.content
                        if content:
                            yield {"content": content}
            else:
                yield {
                    "content": response.choices[0].message.content,
                    "usage": response.usage if hasattr(response, 'usage') else None
                }

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
