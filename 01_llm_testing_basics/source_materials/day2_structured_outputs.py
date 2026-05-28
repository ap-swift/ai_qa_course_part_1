"""
День 2. Structured outputs и JSON validation
===========================================
ЗАДАЧИ:
1. Попросить выбранный provider вернуть JSON.
2. Провалидировать ответ через Pydantic.
3. Безопасно обработать invalid JSON.
4. Начать в mock mode, затем сравнить с Ollama или другим provider.
"""

import json
from pathlib import Path
import sys

from pydantic import BaseModel, ValidationError

sys.path.append(str(Path(__file__).resolve().parents[2] / "code"))

from llm_clients.factory import get_llm_client


class TestCaseEvaluation(BaseModel):
    """Модель данных для оценки ответа test case."""

    score: float
    reasoning: str
    status: str | None = None
    provider: str | None = None


def get_json_response(prompt: str) -> dict:
    """Получить и распарсить JSON-ответ выбранного provider."""
    client = get_llm_client()
    raw_response = client.generate(
        f"Return only valid JSON with fields score, reasoning, status and provider. User task: {prompt}"
    )
    return json.loads(raw_response)


def validate_evaluation(prompt: str) -> TestCaseEvaluation:
    """Провалидировать structured output и показать понятную ошибку."""
    data = get_json_response(prompt)
    return TestCaseEvaluation(**data)


if __name__ == "__main__":
    try:
        result = validate_evaluation("Check whether a chatbot answer follows the expected format.")
        print(result.model_dump())
    except (json.JSONDecodeError, ValidationError) as exc:
        print("Structured output validation завершилась ошибкой.")
        print(exc)
