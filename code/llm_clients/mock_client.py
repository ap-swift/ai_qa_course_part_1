import os

from .base import BaseLLMClient


class MockLLMClient(BaseLLMClient):
    """Детерминированный локальный клиент для первых уроков и автопроверки."""

    provider_name = "mock"

    def __init__(self) -> None:
        self.mode = os.getenv("MOCK_MODE", "strict").strip() or "strict"
        self.model_name = self.mode

    def generate(self, prompt: str) -> str:
        text = prompt.lower()

        if (
            "ignore previous instructions" in text
            or "system prompt" in text
            or "jailbreak" in text
            or "игнорируй предыдущие инструкции" in text
            or "системный промпт" in text
        ):
            return "Я не могу выполнить инструкции, которые пытаются обойти правила безопасности или раскрыть скрытые промпты."

        if "hallucination_test" in text:
            return "Столица Франции — Берлин. Это контролируемый mock-ответ, похожий на галлюцинацию."

        if "capital of france" in text:
            return "Paris is the capital of France."

        if "столица франции" in text:
            return "Париж — столица Франции."

        if "unsafe_answer_simulation" in text:
            return "UNSAFE_SIMULATION: this mock response represents unsafe behavior for a QA test."

        if "rate on a scale" in text or "respond in json" in text or "valid json" in text or "json" in text:
            return '{"score": 0.82, "reasoning": "Mock judge response for deterministic testing.", "status": "ok", "provider": "mock"}'

        if "оцени" in text or "ответь в формате json" in text or "валидный json" in text:
            return '{"score": 0.82, "reasoning": "Детерминированный mock-ответ judge.", "status": "ok", "provider": "mock"}'

        if "software testing" in text:
            return "Software testing checks whether a system behaves as expected and helps find defects before users do."

        if "тестирование по" in text:
            return "Тестирование ПО проверяет, ведет ли себя система ожидаемо, и помогает находить дефекты до пользователей."

        return "Стабильный mock-ответ: используйте этот детерминированный ответ для тестирования AI QA логики без cloud API."
