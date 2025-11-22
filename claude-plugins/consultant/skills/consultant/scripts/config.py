"""
Configuration and constants for oracle Python implementation
"""

import os
from pathlib import Path

# Session storage location
DEFAULT_SESSIONS_DIR = Path.home() / ".oracle-python" / "sessions"

# Default model if none specified and discovery fails
DEFAULT_MODEL = "gpt-5-pro"

# Environment variable names
ENV_LITELLM_API_KEY = "LITELLM_API_KEY"
ENV_OPENAI_API_KEY = "OPENAI_API_KEY"
ENV_ANTHROPIC_API_KEY = "ANTHROPIC_API_KEY"
ENV_OPENAI_BASE_URL = "OPENAI_BASE_URL"

# Token budget: Reserve this percentage for response
CONTEXT_RESERVE_RATIO = 0.2  # 20% reserved for response

# Retry configuration
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 5

# Session polling
POLLING_INTERVAL_SECONDS = 2

# Known model context sizes (fallback if get_max_tokens fails)
KNOWN_CONTEXT_SIZES = {
    "gpt-5-pro": 128000,
    "gpt-5": 128000,
    "gpt-5-mini": 128000,
    "gpt-4o": 128000,
    "gpt-4-turbo": 128000,
    "gpt-4": 8192,
    "gpt-3.5-turbo": 16385,
    "claude-3-5-sonnet-20241022": 200000,
    "claude-3-opus-20240229": 200000,
    "claude-3-sonnet-20240229": 200000,
    "gemini-2.0-flash-exp": 1000000,
}

def get_api_key():
    """Get API key from environment in priority order"""
    return (
        os.environ.get(ENV_LITELLM_API_KEY) or
        os.environ.get(ENV_OPENAI_API_KEY) or
        os.environ.get(ENV_ANTHROPIC_API_KEY)
    )

def get_base_url():
    """Get base URL from OPENAI_BASE_URL environment variable if set"""
    base_url = os.environ.get(ENV_OPENAI_BASE_URL)
    # Only return if non-empty
    return base_url if base_url and base_url.strip() else None
