import os

from .base import BaseLLMClient


class GigaChatClient(BaseLLMClient):
    """Точка интеграции для GigaChat.

    Условия provider, auth flow и SDK могут меняться. Курс показывает структуру
    интеграции, но не притворяется, что непроверенная реализация готова.
    """

    provider_name = "gigachat"

    def __init__(self) -> None:
        self.api_key = os.getenv("GIGACHAT_API_KEY", "").strip()
        self.scope = os.getenv("GIGACHAT_SCOPE", "GIGACHAT_API_PERS").strip()
        self.base_url = os.getenv("GIGACHAT_BASE_URL", "https://gigachat.devices.sberbank.ru/api/v1").rstrip("/")
        self.model_name = "gigachat"

    def generate(self, prompt: str) -> str:
        raise NotImplementedError(
            "GigaChat mode — provider-specific точка интеграции. Проверьте актуальную официальную документацию GigaChat, "
            "храните credentials только в локальном .env, затем реализуйте auth и chat request здесь. "
            "Если ваш аккаунт предоставляет OpenAI-compatible endpoint, используйте LLM_PROVIDER=openai_compatible."
        )
