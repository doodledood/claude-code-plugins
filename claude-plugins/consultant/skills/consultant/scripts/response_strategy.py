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
    from litellm import responses
    LITELLM_AVAILABLE = True
except ImportError:
    LITELLM_AVAILABLE = False

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
                            "usage": result.usage if hasattr(result, 'usage') else None
                        }
                    elif result.status == "failed":
                        error = getattr(result, 'error', 'Unknown error')
                        raise RuntimeError(f"Background job failed: {error}")
                    elif result.status in ["in_progress", "queued"]:
                        # Still processing, wait and retry
                        delay = self._calculate_backoff_delay(
                            attempt,
                            config.POLL_INITIAL_DELAY,
                            config.POLL_MAX_DELAY
                        )
                        time.sleep(delay)
                        attempt += 1
                        continue
                    else:
                        # Unknown status, wait and retry
                        time.sleep(config.POLL_INITIAL_DELAY)
                        continue
                else:
                    # No status field - might be complete already
                    content = self._extract_content(result)
                    if content:
                        return {
                            "content": content,
                            "usage": result.usage if hasattr(result, 'usage') else None
                        }
                    # No content, wait and retry
                    time.sleep(config.POLL_INITIAL_DELAY)
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
                    **kwargs
                )

                content = self._extract_content(response)

                if not content:
                    raise RuntimeError("No content in response from LLM")

                return {
                    "content": content,
                    "usage": response.usage if hasattr(response, 'usage') else None
                }

            except Exception as e:
                error_msg = str(e).lower()

                # Determine if we should retry
                retryable = any(x in error_msg for x in [
                    "network", "timeout", "connection",
                    "429", "rate limit", "too many requests",
                    "503", "service unavailable", "overloaded"
                ])

                # Don't retry auth, context, or validation errors
                non_retryable = any(x in error_msg for x in [
                    "auth", "key", "unauthorized", "forbidden",
                    "context", "token limit", "too long",
                    "not found", "404", "invalid"
                ])

                if non_retryable:
                    # These errors won't be fixed by retrying
                    raise

                if retryable and attempt < config.MAX_RETRIES - 1:
                    # Retry with exponential backoff
                    delay = self._calculate_backoff_delay(
                        attempt,
                        config.INITIAL_RETRY_DELAY,
                        config.MAX_RETRY_DELAY
                    )
                    print(f"Retryable error, waiting {delay:.1f}s before retry {attempt + 2}/{config.MAX_RETRIES}...")
                    time.sleep(delay)
                    continue

                # Final attempt or non-retryable error
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
