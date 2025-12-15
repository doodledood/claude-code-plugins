"""
Response strategies for different LLM providers.
Handles retries, background jobs, and provider-specific quirks.
Automatically detects responses API vs completions API support.
"""

import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import litellm
from litellm import _should_retry, completion, responses

import config


def _is_responses_api_model(model_name: str) -> bool:
    """
    Check if a model name indicates responses API support.

    Uses general patterns that will work for future model versions:
    - GPT-4+ (gpt-4, gpt-5, gpt-6, etc.)
    - O-series reasoning models (o1, o2, o3, o4, etc.)
    - Codex models
    - Computer-use models

    Args:
        model_name: Model name without provider prefix (lowercase)

    Returns:
        True if model should use responses API
    """
    import re

    # GPT-4 and above (gpt-4, gpt-5, gpt-6, etc. but not gpt-3.5)
    # Matches: gpt-4, gpt4, gpt-4-turbo, gpt-5.2, gpt-6-turbo, etc.
    gpt_match = re.search(r"gpt-?(\d+)", model_name)
    if gpt_match:
        version = int(gpt_match.group(1))
        if version >= 4:
            return True

    # O-series reasoning models (o1, o2, o3, o4, etc.)
    # Matches: o1, o1-pro, o3-mini, o4-preview, etc.
    if re.search(r"\bo\d+\b", model_name) or re.search(r"\bo\d+-", model_name):
        return True

    # Codex models (use responses API)
    if "codex" in model_name:
        return True

    # Computer-use models
    return "computer-use" in model_name


def get_responses_api_models() -> set[str]:
    """
    Determine which models support the native OpenAI Responses API.

    Uses litellm.models_by_provider to get OpenAI models, then filters
    to those that support the responses API.

    Returns:
        Set of model identifiers that support the responses API natively.
    """
    responses_models: set[str] = set()

    # Get OpenAI models from litellm
    openai_models = litellm.models_by_provider.get("openai", [])
    azure_models = litellm.models_by_provider.get("azure", [])

    for model in openai_models + azure_models:
        if _is_responses_api_model(model.lower()):
            responses_models.add(model)
            responses_models.add(f"openai/{model}")
            responses_models.add(f"azure/{model}")

    return responses_models


def supports_responses_api(model: str) -> bool:
    """
    Check if a model supports the native OpenAI Responses API.

    Uses general patterns that work for current and future models:
    - GPT-4+ series (gpt-4, gpt-5, gpt-6, etc.)
    - O-series reasoning models (o1, o2, o3, etc.)
    - Codex models
    - Computer-use models

    Args:
        model: Model identifier (e.g., "openai/gpt-4", "gpt-5-mini")

    Returns:
        True if model supports responses API natively, False otherwise.
    """
    model_lower = model.lower()

    # Extract model name and provider
    if "/" in model_lower:
        provider, model_name = model_lower.split("/", 1)
    else:
        provider = "openai"  # Default provider for bare model names
        model_name = model_lower

    # Only OpenAI and Azure support the responses API natively
    if provider not in ("openai", "azure"):
        return False

    # Use the generalized pattern matching
    return _is_responses_api_model(model_name)


class ResponseStrategy(ABC):
    """Base class for response strategies"""

    @abstractmethod
    def execute(
        self,
        model: str,
        prompt: str,
        session_dir: Path | None = None,
        multimodal_content: list[dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Execute LLM request with provider-specific strategy.
        Returns dict with 'content' and optional 'usage'.

        Args:
            model: Model identifier
            prompt: Text prompt
            session_dir: Optional session directory for state persistence
            multimodal_content: Optional multimodal content array for images
            **kwargs: Additional provider-specific arguments
        """
        raise NotImplementedError

    @abstractmethod
    def can_resume(self) -> bool:
        """Whether this strategy supports resuming after failure"""
        raise NotImplementedError

    def _calculate_backoff_delay(
        self, attempt: int, base_delay: int, max_delay: int
    ) -> float:
        """Calculate exponential backoff delay with jitter"""
        import random

        delay = min(base_delay * (2**attempt), max_delay)
        # Add 10% jitter to avoid thundering herd
        jitter = delay * 0.1 * random.random()
        return float(delay + jitter)

    def _extract_content(self, response: Any) -> str:
        """
        Extract text content from response.output structure.

        Handles different output item types:
        - ResponseOutputMessage (type='message'): has content with text
        - ResponseReasoningItem (type='reasoning'): has summary, no content
        """
        content = ""
        if hasattr(response, "output") and response.output:
            for item in response.output:
                # Check item type - only 'message' type has content
                item_type = getattr(item, "type", None)

                if item_type == "message":
                    # ResponseOutputMessage: extract text from content
                    if hasattr(item, "content") and item.content:
                        for content_item in item.content:
                            if hasattr(content_item, "text"):
                                content += content_item.text
                # Skip 'reasoning' items (ResponseReasoningItem) - they have summary, not content
        return content

    def _serialize_usage(self, usage: Any) -> dict[str, Any] | None:
        """
        Safely convert usage object to a JSON-serializable dict.
        Handles Pydantic models (OpenAI), dataclasses, and plain dicts.
        """
        if usage is None:
            return None

        # Already a dict - return as-is
        if isinstance(usage, dict):
            return dict(usage)

        # Pydantic v2 model
        if hasattr(usage, "model_dump"):
            result: dict[str, Any] = usage.model_dump()
            return result

        # Pydantic v1 model
        if hasattr(usage, "dict"):
            result = usage.dict()
            return dict(result)

        # Dataclass or object with __dict__
        if hasattr(usage, "__dict__"):
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

    def _convert_to_responses_api_format(
        self, multimodal_content: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """
        Convert multimodal content from Completions API format to Responses API format.

        Completions format: [{"type": "text/image_url", ...}]
        Responses format: [{"type": "input_text/input_image", ...}]
        """
        converted: list[dict[str, Any]] = []
        for item in multimodal_content:
            item_type = item.get("type", "")
            if item_type == "text":
                converted.append({"type": "input_text", "text": item.get("text", "")})
            elif item_type == "image_url":
                # Extract URL from nested object
                image_url = item.get("image_url", {})
                url = image_url.get("url", "") if isinstance(image_url, dict) else ""
                converted.append({"type": "input_image", "image_url": url})
        return converted

    def execute(
        self,
        model: str,
        prompt: str,
        session_dir: Path | None = None,
        multimodal_content: list[dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Execute with background job and polling"""

        response_id_file = session_dir / "response_id.txt" if session_dir else None

        # Check if we're resuming an existing background job
        if response_id_file and response_id_file.exists():
            response_id = response_id_file.read_text().strip()
            print(f"Resuming background job: {response_id}")
            return self._poll_for_completion(response_id)

        # Build input - convert multimodal to Responses API format if provided
        input_content: str | list[dict[str, Any]]
        if multimodal_content:
            input_content = self._convert_to_responses_api_format(multimodal_content)
        else:
            input_content = prompt

        # Start new background job
        try:
            response = responses(
                model=model,
                input=input_content,
                background=True,  # Returns immediately with response_id
                num_retries=config.MAX_RETRIES,  # Use LiteLLM's built-in retries
                **kwargs,
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
            raise RuntimeError(f"Background job failed to start: {e}") from e

    def _poll_for_completion(self, response_id: str) -> dict[str, Any]:
        """Poll for completion with exponential backoff and retries"""

        start_time = time.time()
        attempt = 0

        while time.time() - start_time < config.POLL_TIMEOUT:
            try:
                # Retrieve the response by ID
                result = litellm.get_response(response_id=response_id)

                if hasattr(result, "status"):
                    if result.status == "completed":
                        content = self._extract_content(result)
                        if not content:
                            raise RuntimeError("No content in completed response")
                        return {
                            "content": content,
                            "usage": self._serialize_usage(
                                getattr(result, "usage", None)
                            ),
                            "response": result,  # Include full response for cost calculation
                        }
                    elif result.status == "failed":
                        error = getattr(result, "error", "Unknown error")
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
                            "usage": self._serialize_usage(
                                getattr(result, "usage", None)
                            ),
                            "response": result,  # Include full response for cost calculation
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
                            attempt, config.INITIAL_RETRY_DELAY, config.MAX_RETRY_DELAY
                        )
                        print(
                            f"Network error polling job, retrying in {delay:.1f}s... (attempt {attempt + 1}/{config.MAX_RETRIES})"
                        )
                        time.sleep(delay)
                        attempt += 1
                        continue
                    else:
                        raise RuntimeError(
                            f"Network errors exceeded max retries: {e}"
                        ) from e

                # Other errors - raise immediately
                raise

        raise TimeoutError(
            f"Background job {response_id} did not complete within {config.POLL_TIMEOUT}s"
        )

    def can_resume(self) -> bool:
        return True


class SyncRetryStrategy(ResponseStrategy):
    """
    For OpenAI/Azure models using responses API - direct sync calls with retry logic.
    Cannot resume - must retry from scratch if it fails.
    """

    def _convert_to_responses_api_format(
        self, multimodal_content: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """
        Convert multimodal content from Completions API format to Responses API format.

        Completions format: [{"type": "text/image_url", ...}]
        Responses format: [{"type": "input_text/input_image", ...}]
        """
        converted: list[dict[str, Any]] = []
        for item in multimodal_content:
            item_type = item.get("type", "")
            if item_type == "text":
                converted.append({"type": "input_text", "text": item.get("text", "")})
            elif item_type == "image_url":
                # Extract URL from nested object
                image_url = item.get("image_url", {})
                url = image_url.get("url", "") if isinstance(image_url, dict) else ""
                converted.append({"type": "input_image", "image_url": url})
        return converted

    def execute(
        self,
        model: str,
        prompt: str,
        session_dir: Path | None = None,
        multimodal_content: list[dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Execute with synchronous retries using responses API"""

        # Build input - convert multimodal to Responses API format if provided
        input_content: str | list[dict[str, Any]]
        if multimodal_content:
            input_content = self._convert_to_responses_api_format(multimodal_content)
        else:
            input_content = prompt

        for attempt in range(config.MAX_RETRIES):
            try:
                response = responses(
                    model=model,
                    input=input_content,
                    stream=False,
                    num_retries=config.MAX_RETRIES,  # Use LiteLLM's built-in retries
                    **kwargs,
                )

                content = self._extract_content(response)

                if not content:
                    raise RuntimeError("No content in response from LLM")

                return {
                    "content": content,
                    "usage": self._serialize_usage(getattr(response, "usage", None)),
                    "response": response,  # Include full response for cost calculation
                }

            except Exception as e:
                # Use LiteLLM's built-in retry logic for HTTP errors
                if _should_retry and hasattr(e, "status_code"):
                    retryable = _should_retry(e.status_code)
                else:
                    # Fallback to string matching for non-HTTP errors
                    error_msg = str(e).lower()
                    retryable = any(
                        x in error_msg
                        for x in [
                            "network",
                            "timeout",
                            "connection",
                            "429",
                            "rate limit",
                            "503",
                            "overloaded",
                        ]
                    )
                    non_retryable = any(
                        x in error_msg
                        for x in [
                            "auth",
                            "key",
                            "context",
                            "token limit",
                            "not found",
                            "invalid",
                        ]
                    )

                    if non_retryable:
                        raise

                if retryable and attempt < config.MAX_RETRIES - 1:
                    delay = self._calculate_backoff_delay(
                        attempt, config.INITIAL_RETRY_DELAY, config.MAX_RETRY_DELAY
                    )
                    print(
                        f"Retryable error, waiting {delay:.1f}s before retry {attempt + 2}/{config.MAX_RETRIES}..."
                    )
                    time.sleep(delay)
                    continue

                raise

        raise RuntimeError("Max retries exceeded")

    def can_resume(self) -> bool:
        return False


class CompletionsAPIStrategy(ResponseStrategy):
    """
    For Anthropic/Google/other providers - uses chat completions API directly.
    More efficient than bridging through responses API for non-OpenAI providers.
    """

    def execute(
        self,
        model: str,
        prompt: str,
        session_dir: Path | None = None,
        multimodal_content: list[dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Execute with chat completions API"""

        # Remove responses-specific kwargs that don't apply to completions
        kwargs.pop("reasoning_effort", None)
        kwargs.pop("background", None)

        # Build message content - use multimodal content if provided, else plain prompt
        message_content: str | list[dict[str, Any]] = (
            multimodal_content if multimodal_content else prompt
        )

        for attempt in range(config.MAX_RETRIES):
            try:
                # Use chat completions API
                response = completion(
                    model=model,
                    messages=[{"role": "user", "content": message_content}],
                    stream=False,
                    num_retries=config.MAX_RETRIES,
                    **kwargs,
                )

                # Extract content from chat completion response
                content = self._extract_completion_content(response)

                if not content:
                    raise RuntimeError("No content in response from LLM")

                return {
                    "content": content,
                    "usage": self._serialize_usage(getattr(response, "usage", None)),
                    "response": response,
                }

            except Exception as e:
                # Use LiteLLM's built-in retry logic for HTTP errors
                if _should_retry and hasattr(e, "status_code"):
                    retryable = _should_retry(e.status_code)
                else:
                    error_msg = str(e).lower()
                    retryable = any(
                        x in error_msg
                        for x in [
                            "network",
                            "timeout",
                            "connection",
                            "429",
                            "rate limit",
                            "503",
                            "overloaded",
                        ]
                    )
                    non_retryable = any(
                        x in error_msg
                        for x in [
                            "auth",
                            "key",
                            "context",
                            "token limit",
                            "not found",
                            "invalid",
                        ]
                    )

                    if non_retryable:
                        raise

                if retryable and attempt < config.MAX_RETRIES - 1:
                    delay = self._calculate_backoff_delay(
                        attempt, config.INITIAL_RETRY_DELAY, config.MAX_RETRY_DELAY
                    )
                    print(
                        f"Retryable error, waiting {delay:.1f}s before retry {attempt + 2}/{config.MAX_RETRIES}..."
                    )
                    time.sleep(delay)
                    continue

                raise

        raise RuntimeError("Max retries exceeded")

    def _extract_completion_content(self, response: Any) -> str:
        """Extract text content from chat completions response"""
        if hasattr(response, "choices") and response.choices:
            choice = response.choices[0]
            if hasattr(choice, "message") and hasattr(choice.message, "content"):
                return choice.message.content or ""
        return ""

    def can_resume(self) -> bool:
        return False


class ResponseStrategyFactory:
    """Factory to select appropriate strategy based on model/provider and API support"""

    # Models/providers that support background jobs (OpenAI Responses API feature)
    BACKGROUND_SUPPORTED = {
        "openai/",
        "azure/",
    }

    @staticmethod
    def get_strategy(model: str) -> ResponseStrategy:
        """
        Select strategy based on model capabilities and API support.

        Decision tree:
        1. If model supports responses API AND background jobs -> BackgroundJobStrategy
        2. If model supports responses API (no background) -> SyncRetryStrategy
        3. If model doesn't support responses API -> CompletionsAPIStrategy

        Uses litellm.models_by_provider to determine support.
        """
        # Check if model supports native responses API
        if supports_responses_api(model):
            # Check if it also supports background jobs
            if ResponseStrategyFactory.supports_background(model):
                return BackgroundJobStrategy()
            return SyncRetryStrategy()

        # For all other providers (Anthropic, Google, Bedrock, etc.)
        # Use completions API directly - more efficient than bridging
        return CompletionsAPIStrategy()

    @staticmethod
    def supports_background(model: str) -> bool:
        """Check if model supports background job execution (OpenAI/Azure only)"""
        model_lower = model.lower()
        return any(
            model_lower.startswith(prefix)
            for prefix in ResponseStrategyFactory.BACKGROUND_SUPPORTED
        )

    @staticmethod
    def get_api_type(model: str) -> str:
        """
        Determine which API type will be used for a given model.

        Returns:
            'responses' for models using OpenAI Responses API
            'completions' for models using Chat Completions API
        """
        if supports_responses_api(model):
            return "responses"
        return "completions"
