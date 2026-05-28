import os
from typing import Any

import requests

from .base import BaseLLMClient, LLMClientError


class OllamaClient(BaseLLMClient):
    """Клиент для локальных моделей Ollama через `/api/generate`."""

    provider_name = "ollama"

    def __init__(self) -> None:
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")
        self.model_name = os.getenv("OLLAMA_MODEL", "qwen2.5:7b").strip() or "qwen2.5:7b"

    def generate(self, prompt: str) -> str:
        payload: dict[str, Any] = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
        }
        try:
            response = requests.post(f"{self.base_url}/api/generate", json=payload, timeout=120)
            response.raise_for_status()
        except requests.ConnectionError as exc:
            raise LLMClientError(
                "Ollama недоступен. Запустите: `ollama serve`. "
                "Затем скачайте модель, например: `ollama pull qwen2.5:7b`."
            ) from exc
        except requests.HTTPError as exc:
            raise LLMClientError(
                f"Ollama вернул HTTP {response.status_code}. Проверьте, что модель `{self.model_name}` установлена. "
                f"Попробуйте: `ollama pull {self.model_name}`."
            ) from exc
        except requests.RequestException as exc:
            raise LLMClientError(f"Запрос к Ollama завершился ошибкой: {exc}") from exc

        data = response.json()
        return str(data.get("response", "")).strip()
