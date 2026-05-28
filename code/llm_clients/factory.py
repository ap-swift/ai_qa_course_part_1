import os

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover
    load_dotenv = None

from .base import BaseLLMClient, LLMClientError
from .gigachat_client import GigaChatClient
from .mock_client import MockLLMClient
from .ollama_client import OllamaClient
from .openai_compatible_client import OpenAICompatibleClient
from .yandexgpt_client import YandexGPTClient


def get_llm_client() -> BaseLLMClient:
    """Создать LLM client по значению LLM_PROVIDER из локального `.env`."""
    if load_dotenv is not None:
        load_dotenv()

    provider = os.getenv("LLM_PROVIDER", "mock").strip().lower()

    if provider == "mock":
        return MockLLMClient()
    if provider == "ollama":
        return OllamaClient()
    if provider == "gigachat":
        return GigaChatClient()
    if provider == "yandexgpt":
        return YandexGPTClient()
    if provider == "russian_cloud":
        raise LLMClientError(
            "Используйте LLM_PROVIDER=gigachat или LLM_PROVIDER=yandexgpt для российских cloud-примеров, "
            "или openai_compatible, если provider предоставляет совместимый endpoint."
        )
    if provider == "openai_compatible":
        return OpenAICompatibleClient()

    raise LLMClientError(
        f"Неизвестный LLM_PROVIDER={provider!r}. Доступные значения: "
        "mock, ollama, gigachat, yandexgpt, openai_compatible."
    )
