"""
День 5. Promptfoo — Быстрый старт (companion-скрипт)
=====================================================
Этот скрипт показывает, как запускать promptfoo программно из Python
и как интегрировать его в ваш рабочий процесс.

УСТАНОВКА:
  npm install -g promptfoo
  ИЛИ
  npx promptfoo@latest eval -c week1-llm-basics/day5_promptfoo.yaml

ПРОСМОТР РЕЗУЛЬТАТОВ:
  npx promptfoo view

ЗАДАЧИ:
1. Запустить YAML-конфигурацию и изучить веб-интерфейс
2. Изменить prompt (v1 vs v2) и проверить, какие тест-кейсы сломались
3. Добавить нового провайдера (например, openai:gpt-4o) для сравнения моделей
4. Экспортировать результаты: npx promptfoo eval --output results.json
"""

import subprocess
import json
import os


def run_promptfoo_eval(config_path: str = "week1-llm-basics/day5_promptfoo.yaml"):
    """Запустить promptfoo evaluation и вернуть результаты."""
    output_path = "week1-llm-basics/outputs/day5_promptfoo_results.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    cmd = [
        "npx", "promptfoo", "eval",
        "-c", config_path,
        "--output", output_path,
    ]
    print(f"Запуск: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Ошибка: {result.stderr}")
        return None

    print(result.stdout)
    if os.path.exists(output_path):
        with open(output_path) as f:
            return json.load(f)
    return None


def analyze_results(results: dict):
    """Проанализировать результаты promptfoo и выделить провалы."""
    if not results:
        print("Нет результатов для анализа.")
        return

    print("\n=== АНАЛИЗ РЕЗУЛЬТАТОВ PROMPTFOO ===")
    total = 0
    passed = 0
    failed_cases = []

    for result in results.get("results", {}).get("results", []):
        total += 1
        if result.get("success"):
            passed += 1
        else:
            failed_cases.append({
                "prompt": result.get("vars", {}).get("question", "?")[:50],
                "failures": [a.get("reason", "unknown") for a in result.get("assertionResults", []) if not a.get("pass")],
            })

    print(f"Всего: {total} | Пройдено: {passed} | Провалено: {total - passed}")
    if failed_cases:
        print("\nПровалившиеся кейсы:")
        for fc in failed_cases:
            print(f"  - {fc['prompt']}")
            for reason in fc["failures"]:
                print(f"    ! {reason[:80]}")


if __name__ == "__main__":
    print("=== День 5: Promptfoo Evaluation ===")
    print("\nДля запуска evaluation:")
    print("  npx promptfoo eval -c week1-llm-basics/day5_promptfoo.yaml")
    print("\nДля просмотра результатов в браузере:")
    print("  npx promptfoo view")
    print("\nДля программного запуска (нужен npx в PATH):")

    results = run_promptfoo_eval()
    if results:
        analyze_results(results)
