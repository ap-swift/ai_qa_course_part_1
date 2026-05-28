from abc import ABC, abstractmethod


class LLMClientError(RuntimeError):
    """Ошибка настройки provider или выполнения запроса."""


class BaseLLMClient(ABC):
    """Минимальный интерфейс для учебных примеров.

    Курс обучает AI QA methodology, поэтому примеры зависят только от
    `generate()`, а не от SDK конкретного vendor.
    """

    provider_name = "base"
    model_name = "unknown"

    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass
