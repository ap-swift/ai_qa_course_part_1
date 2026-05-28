import os
from typing import Any

import requests

from .base import BaseLLMClient, LLMClientError


class OpenAICompatibleClient(BaseLLMClient):
    """Универсальный клиент для providers с OpenAI-compatible chat API.

    Название описывает стандарт API, а не требование использовать OpenAI.
    """

    provider_name = "openai_compatible"

    def __init__(self) -> None:
        self.base_url = os.getenv("OPENAI_COMPATIBLE_BASE_URL", "").rstrip("/")
        self.api_key = os.getenv("OPENAI_COMPATIBLE_API_KEY", "").strip()
        self.model_name = os.getenv("OPENAI_COMPATIBLE_MODEL", "").strip()
        if not self.base_url or not self.api_key or not self.model_name:
            raise LLMClientError(
                "Укажите OPENAI_COMPATIBLE_BASE_URL, OPENAI_COMPATIBLE_API_KEY и "
                "OPENAI_COMPATIBLE_MODEL в локальном .env. Не отправляйте эти значения в Stepik или GitHub."
            )

    def generate(self, prompt: str) -> str:
        payload: dict[str, Any] = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0,
        }
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        try:
            response = requests.post(f"{self.base_url}/chat/completions", json=payload, headers=headers, timeout=120)
            response.raise_for_status()
        except requests.RequestException as exc:
            raise LLMClientError(
                "OpenAI-compatible запрос завершился ошибкой. Проверьте endpoint, model name, доступ аккаунта и локальный .env. "
                "Никогда не вставляйте API-ключи в поля Stepik или GitHub."
            ) from exc

        data = response.json()
        try:
            return data["choices"][0]["message"]["content"].strip()
        except (KeyError, IndexError, TypeError) as exc:
            raise LLMClientError(f"Неожиданный формат OpenAI-compatible ответа: {data}") from exc
