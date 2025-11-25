"""
Model discovery and selection logic
"""

from typing import Any

import requests
from litellm import model_cost


class ModelSelector:
    """Handles model discovery and automatic selection"""

    @staticmethod
    def list_models(base_url: str | None = None) -> list[dict[str, Any]]:
        """
        Query available models.

        Without base_url: Uses LiteLLM's model_cost dictionary for dynamic discovery
        With base_url: Calls proxy's /models or /v1/models endpoint
        """

        if not base_url:
            # Use LiteLLM's model_cost for dynamic discovery
            return ModelSelector._get_litellm_models()

        # Try LiteLLM proxy /models endpoint first, then OpenAI-compatible /v1/models
        last_error = None
        for endpoint in ["/models", "/v1/models"]:
            try:
                models_url = f"{base_url.rstrip('/')}{endpoint}"
                response = requests.get(models_url, timeout=10)
                response.raise_for_status()

                data = response.json()
                models = data.get("data", [])

                return [
                    {
                        "id": m.get("id"),
                        "created": m.get("created"),
                        "owned_by": m.get("owned_by"),
                    }
                    for m in models
                ]
            except Exception as e:
                last_error = e
                continue

        # If all endpoints fail, raise an error
        raise RuntimeError(f"Could not fetch models from {base_url}: {last_error}")

    @staticmethod
    def select_best_model(base_url: str | None = None) -> str:
        """
        Automatically select the best available model.
        Heuristic: Prefer models with "large", "pro", or higher version numbers
        """

        models = ModelSelector.list_models(base_url)

        if not models:
            raise RuntimeError("No models available - cannot auto-select model")

        # Score models based on name heuristics
        best_model = max(models, key=ModelSelector._score_model)
        model_id = best_model.get("id")
        if not model_id:
            raise RuntimeError("Best model has no id - cannot auto-select model")
        return str(model_id)

    @staticmethod
    def _score_model(model: dict[str, Any]) -> float:
        """Score a model based on capabilities (higher is better)"""

        model_id = model.get("id", "").lower()
        score = 0.0

        # Version number scoring
        if "gpt-5" in model_id or "o1" in model_id or "o3" in model_id:
            score += 50
        elif "gpt-4" in model_id:
            score += 40
        elif "gpt-3.5" in model_id:
            score += 30

        # Capability indicators
        if any(x in model_id for x in ["pro", "turbo", "large", "xl", "ultra"]):
            score += 20

        # Context size indicators
        if "128k" in model_id or "200k" in model_id:
            score += 15
        elif "32k" in model_id:
            score += 12
        elif "16k" in model_id:
            score += 10

        # Anthropic models
        if "claude" in model_id:
            if "opus" in model_id:
                score += 50
            elif "sonnet" in model_id:
                if "3.5" in model_id or "3-5" in model_id:
                    score += 48
                else:
                    score += 45
            elif "haiku" in model_id:
                score += 35

        # Google models
        if "gemini" in model_id:
            if "2.0" in model_id or "2-0" in model_id:
                score += 45
            elif "pro" in model_id:
                score += 40

        return score

    @staticmethod
    def _get_litellm_models() -> list[dict[str, Any]]:
        """
        Get models from LiteLLM's model_cost dictionary.
        This provides dynamic model discovery without hardcoded lists.
        """

        if not model_cost:
            raise RuntimeError("LiteLLM model_cost is empty - cannot discover models")

        # Convert model_cost dictionary to list format
        models = []
        for model_id, info in model_cost.items():
            models.append(
                {
                    "id": model_id,
                    "provider": info.get("litellm_provider", "unknown"),
                    "max_tokens": info.get("max_tokens"),
                    "input_cost_per_token": info.get("input_cost_per_token"),
                    "output_cost_per_token": info.get("output_cost_per_token"),
                }
            )

        return models
