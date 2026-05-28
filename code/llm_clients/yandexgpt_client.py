import os

from .base import BaseLLMClient


class YandexGPTClient(BaseLLMClient):
    """Точка интеграции для YandexGPT."""

    provider_name = "yandexgpt"

    def __init__(self) -> None:
        self.api_key = os.getenv("YANDEX_API_KEY", "").strip()
        self.folder_id = os.getenv("YANDEX_FOLDER_ID", "").strip()
        self.model_uri = os.getenv("YANDEX_MODEL_URI", "").strip()
        self.model_name = self.model_uri or "yandexgpt"

    def generate(self, prompt: str) -> str:
        raise NotImplementedError(
            "YandexGPT mode — provider-specific точка интеграции. Проверьте актуальную документацию Yandex Cloud, "
            "храните credentials только в локальном .env, затем реализуйте completion request здесь. "
            "Если ваш аккаунт предоставляет OpenAI-compatible endpoint, используйте LLM_PROVIDER=openai_compatible."
        )
