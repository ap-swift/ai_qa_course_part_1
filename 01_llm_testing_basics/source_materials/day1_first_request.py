"""
День 1. Первый LLM-запрос и настройка provider
=========================================
ЗАДАЧИ:
1. Начать с LLM_PROVIDER=mock, без cloud API.
2. Запустить скрипт и проверить provider layer.
3. Позже переключиться на Ollama или другой provider и сравнить ответы.
4. ДОПОЛНИТЕЛЬНОЕ ЗАДАНИЕ: добавить новый prompt и сравнить два providers на одном input.

ЧТО ИЗУЧАЕМ:
- Курс тестирует поведение AI, а не конкретного vendor.
- `mock` детерминирован и подходит для первых tests/autochecks.
- Ollama или cloud providers подключаются через `llm_clients`.
- Никогда не вставляйте API-ключи в Stepik, GitHub, отчеты или screenshots.
"""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[2] / "code"))

from llm_clients.factory import get_llm_client


def basic_request(prompt: str) -> str:
    """Отправить базовый provider-agnostic запрос."""
    client = get_llm_client()
    return client.generate(prompt)


def compare_repeated_runs(prompt: str, runs: int = 3) -> None:
    """Запустить один prompt несколько раз и сравнить стабильность.

    В `mock`-режиме ответы детерминированы. Реальные модели могут отличаться
    из-за настроек provider. В отчете фиксируйте provider/model, но не API-ключи.
    """
    client = get_llm_client()
    print(f"Provider: {client.provider_name}")
    print(f"Model: {getattr(client, 'model_name', 'unknown')}")
    print(f"Prompt: {prompt}")
    for idx in range(1, runs + 1):
        print(f"\n--- Run {idx} ---")
        print(client.generate(prompt))


if __name__ == "__main__":
    print("=== ЗАДАЧА 1: smoke request через provider ===")
    print(basic_request("What is software testing in one sentence?"))

    print("\n=== ЗАДАЧА 2: проверка стабильности ===")
    compare_repeated_runs("Invent a concise name for a startup that tests AI systems.")
