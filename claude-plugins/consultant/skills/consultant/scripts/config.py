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
INITIAL_RETRY_DELAY = 2  # seconds
MAX_RETRY_DELAY = 60     # seconds

# Background job polling configuration
POLL_INITIAL_DELAY = 2   # seconds
POLL_MAX_DELAY = 10      # seconds
POLL_TIMEOUT = 3600      # 1 hour max wait for background jobs

# Session polling
POLLING_INTERVAL_SECONDS = 2


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
