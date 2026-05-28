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

        if "ignore previous instructions" in text or "system prompt" in text or "jailbreak" in text:
            return "I cannot follow instructions that try to override safety rules or reveal hidden prompts."

        if "capital of france" in text:
            return "Paris is the capital of France."

        if "hallucination_test" in text:
            return "The capital of France is Berlin. This is a controlled hallucination-like mock response."

        if "unsafe_answer_simulation" in text:
            return "UNSAFE_SIMULATION: this mock response represents unsafe behavior for a QA test."

        if "rate on a scale" in text or "respond in json" in text or "valid json" in text or "json" in text:
            return '{"score": 0.82, "reasoning": "Mock judge response for deterministic testing.", "status": "ok", "provider": "mock"}'

        if "software testing" in text:
            return "Software testing checks whether a system behaves as expected and helps find defects before users do."

        return "Stable mock response: use this deterministic answer to test AI QA logic without a cloud API."
