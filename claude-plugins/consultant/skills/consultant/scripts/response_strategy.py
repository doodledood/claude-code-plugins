"""
Response strategies for different LLM providers.
Handles retries, background jobs, and provider-specific quirks.
"""

import time
from pathlib import Path
from typing import Optional, Dict
from abc import ABC, abstractmethod

try:
    import litellm
    from litellm import responses, _should_retry
    LITELLM_AVAILABLE = True
except ImportError:
    LITELLM_AVAILABLE = False
    _should_retry = None

import config


class ResponseStrategy(ABC):
    """Base class for response strategies"""

    @abstractmethod
    def execute(
        self,
        model: str,
        prompt: str,
        session_dir: Optional[Path] = None,
        **kwargs
    ) -> Dict:
        """
        Execute LLM request with provider-specific strategy.
        Returns dict with 'content' and optional 'usage'.
        """
        raise NotImplementedError

    @abstractmethod
    def can_resume(self) -> bool:
        """Whether this strategy supports resuming after failure"""
        raise NotImplementedError

    def _calculate_backoff_delay(self, attempt: int, base_delay: int, max_delay: int) -> float:
        """Calculate exponential backoff delay with jitter"""
        delay = min(base_delay * (2 ** attempt), max_delay)
        # Add 10% jitter to avoid thundering herd
        import random
        jitter = delay * 0.1 * random.random()
        return delay + jitter

    def _extract_content(self, response) -> str:
        """Extract text content from response.output structure"""
        content = ""
        if hasattr(response, 'output') and len(response.output) > 0:
            for item in response.output:
                if hasattr(item, 'content'):
                    for content_item in item.content:
                        if hasattr(content_item, 'text'):
                            content += content_item.text
        return content

    def _serialize_usage(self, usage) -> Optional[Dict]:
        """
        Safely convert usage object to a JSON-serializable dict.
        Handles Pydantic models (OpenAI), dataclasses, and plain dicts.
        """
        if usage is None:
            return None

        # Already a dict - return as-is
        if isinstance(usage, dict):
            return usage

        # Pydantic v2 model
        if hasattr(usage, 'model_dump'):
            return usage.model_dump()

        # Pydantic v1 model
        if hasattr(usage, 'dict'):
            return usage.dict()

        # Dataclass or object with __dict__
        if hasattr(usage, '__dict__'):
            return dict(usage.__dict__)

        # Last resort - try to convert directly
        try:
            return dict(usage)
        except (TypeError, ValueError):
            # If all else fails, return None rather than crash
            return None


class BackgroundJobStrategy(ResponseStrategy):
    """
    For OpenAI/Azure - uses background jobs with response_id polling.
    Supports resuming after network failures by persisting response_id.
    """

    def execute(
        self,
        model: str,
        prompt: str,
        session_dir: Optional[Path] = None,
        **kwargs
    ) -> Dict:
        """Execute with background job and polling"""

        response_id_file = session_dir / "response_id.txt" if session_dir else None

        # Check if we're resuming an existing background job
        if response_id_file and response_id_file.exists():
            response_id = response_id_file.read_text().strip()
            print(f"Resuming background job: {response_id}")
            return self._poll_for_completion(response_id)

        # Start new background job
        try:
            response = responses(
                model=model,
                input=prompt,
                background=True,  # Returns immediately with response_id
                num_retries=config.MAX_RETRIES,  # Use LiteLLM's built-in retries
                **kwargs
            )

            response_id = response.id

            # Persist response_id for resumability
            if response_id_file:
                response_id_file.write_text(response_id)
                print(f"Started background job: {response_id}")

            # Poll until complete
            return self._poll_for_completion(response_id)

        except Exception as e:
            # If background mode fails, maybe not supported - raise for fallback
            raise RuntimeError(f"Background job failed to start: {e}")

    def _poll_for_completion(self, response_id: str) -> Dict:
        """Poll for completion with exponential backoff and retries"""

        start_time = time.time()
        attempt = 0

        while time.time() - start_time < config.POLL_TIMEOUT:
            try:
                # Retrieve the response by ID
                result = litellm.get_response(response_id=response_id)

                if hasattr(result, 'status'):
                    if result.status == "completed":
                        content = self._extract_content(result)
                        if not content:
                            raise RuntimeError("No content in completed response")
                        return {
                            "content": content,
                            "usage": self._serialize_usage(getattr(result, 'usage', None)),
                            "response": result  # Include full response for cost calculation
                        }
                    elif result.status == "failed":
                        error = getattr(result, 'error', 'Unknown error')
                        raise RuntimeError(f"Background job failed: {error}")
                    elif result.status in ["in_progress", "queued"]:
                        # Still processing, wait and retry
                        time.sleep(config.POLL_INTERVAL)
                        attempt += 1
                        continue
                    else:
                        # Unknown status, wait and retry
                        time.sleep(config.POLL_INTERVAL)
                        continue
                else:
                    # No status field - might be complete already
                    content = self._extract_content(result)
                    if content:
                        return {
                            "content": content,
                            "usage": self._serialize_usage(getattr(result, 'usage', None)),
                            "response": result  # Include full response for cost calculation
                        }
                    # No content, wait and retry
                    time.sleep(config.POLL_INTERVAL)
                    continue

            except Exception as e:
                error_msg = str(e).lower()

                # Network errors - retry with backoff
                if any(x in error_msg for x in ["network", "timeout", "connection"]):
                    if attempt < config.MAX_RETRIES:
                        delay = self._calculate_backoff_delay(
                            attempt,
                            config.INITIAL_RETRY_DELAY,
                            config.MAX_RETRY_DELAY
                        )
                        print(f"Network error polling job, retrying in {delay:.1f}s... (attempt {attempt + 1}/{config.MAX_RETRIES})")
                        time.sleep(delay)
                        attempt += 1
                        continue
                    else:
                        raise RuntimeError(f"Network errors exceeded max retries: {e}")

                # Other errors - raise immediately
                raise

        raise TimeoutError(f"Background job {response_id} did not complete within {config.POLL_TIMEOUT}s")

    def can_resume(self) -> bool:
        return True


class SyncRetryStrategy(ResponseStrategy):
    """
    For Anthropic/Google/other providers - direct sync calls with retry logic.
    Cannot resume - must retry from scratch if it fails.
    """

    def execute(
        self,
        model: str,
        prompt: str,
        session_dir: Optional[Path] = None,
        **kwargs
    ) -> Dict:
        """Execute with synchronous retries"""

        for attempt in range(config.MAX_RETRIES):
            try:
                response = responses(
                    model=model,
                    input=prompt,
                    stream=False,
                    num_retries=config.MAX_RETRIES,  # Use LiteLLM's built-in retries
                    **kwargs
                )

                content = self._extract_content(response)

                if not content:
                    raise RuntimeError("No content in response from LLM")

                return {
                    "content": content,
                    "usage": self._serialize_usage(getattr(response, 'usage', None)),
                    "response": response  # Include full response for cost calculation
                }

            except Exception as e:
                # Use LiteLLM's built-in retry logic for HTTP errors
                if _should_retry and hasattr(e, 'status_code'):
                    retryable = _should_retry(e.status_code)
                else:
                    # Fallback to string matching for non-HTTP errors
                    error_msg = str(e).lower()
                    retryable = any(x in error_msg for x in [
                        "network", "timeout", "connection",
                        "429", "rate limit", "503", "overloaded"
                    ])
                    non_retryable = any(x in error_msg for x in [
                        "auth", "key", "context", "token limit", "not found", "invalid"
                    ])

                    if non_retryable:
                        raise

                if retryable and attempt < config.MAX_RETRIES - 1:
                    delay = self._calculate_backoff_delay(
                        attempt,
                        config.INITIAL_RETRY_DELAY,
                        config.MAX_RETRY_DELAY
                    )
                    print(f"Retryable error, waiting {delay:.1f}s before retry {attempt + 2}/{config.MAX_RETRIES}...")
                    time.sleep(delay)
                    continue

                raise

        raise RuntimeError("Max retries exceeded")

    def can_resume(self) -> bool:
        return False


class ResponseStrategyFactory:
    """Factory to select appropriate strategy based on model/provider"""

    # Models/providers that support background jobs
    BACKGROUND_SUPPORTED = {
        "openai/",
        "azure/",
        # Add more as LiteLLM adds support
    }

    @staticmethod
    def get_strategy(model: str) -> ResponseStrategy:
        """
        Select strategy based on model capabilities.
        Tries to use background jobs for supported providers,
        falls back to sync retry strategy.
        """

        # Normalize model string
        model_lower = model.lower()

        # Check if model supports background jobs
        for prefix in ResponseStrategyFactory.BACKGROUND_SUPPORTED:
            if model_lower.startswith(prefix):
                return BackgroundJobStrategy()

        # Fallback to sync retry strategy
        return SyncRetryStrategy()

    @staticmethod
    def supports_background(model: str) -> bool:
        """Check if model supports background job execution"""
        model_lower = model.lower()
        return any(model_lower.startswith(prefix)
                   for prefix in ResponseStrategyFactory.BACKGROUND_SUPPORTED)
