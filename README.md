# AI QA Engineer: тестирование LLM на Python

Практический курс для QA-инженеров и Python-разработчиков, которые хотят научиться тестировать LLM-приложения и AI-ботов.

## Чему вы научитесь

- Писать тест-кейсы для LLM-ответов: качество, формат, полнота, устойчивость
- Строить regression suite для промптов с `pytest` и `promptfoo`
- Проверять hallucinations с помощью DeepEval
- Использовать evaluation metrics: BLEU, ROUGE, cosine similarity
- Тестировать prompt injection, jailbreak, indirect injection
- Проводить red teaming и строить guardrails
- Тестировать consistency и bias моделей
- Подключать AI QA-проверки к GitHub Actions

## Структура курса

```
00_course_overview/               — установка и настройка
01_llm_testing_basics/            — основы тестирования LLM
02_prompt_injection_and_security/ — security testing и CI/CD
code/                             — provider layer и утилиты
final_project/                    — финальный проект
```

## Prerequisites

- Python 3.10+
- Основы QA: test cases, expected result, regression testing
- Понимание API: request/response, JSON, environment variables
- Базовый Git/GitHub (желательно)

## Быстрый старт

```bash
git clone https://github.com/ap-swift/ai_qa_course_part_1.git
cd stepik_course_package
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r code/requirements.txt
cp .env.example .env
python code/smoke_test_llm_provider.py
```

## Выбор LLM-провайдера

Курс не привязан к конкретному провайдеру. Модель — заменяемый слой.

| Режим | Описание | API-ключ |
|---|---|---|
| `mock` | Фиксированные ответы, для старта | Не нужен |
| `ollama` | Локальные модели (qwen2.5, llama3, mistral) | Не нужен |
| `gigachat` | Облачный провайдер | Нужен |
| `yandexgpt` | Облачный провайдер | Нужен |
| `openai_compatible` | Любой совместимый API | Нужен |

Рекомендуемый путь:

1. Начать с `LLM_PROVIDER=mock`
2. Установить Ollama для реальных экспериментов
3. При желании подключить облачный провайдер

## Запуск

```bash
# Smoke test
python code/smoke_test_llm_provider.py

# Модуль 1: основы LLM testing
python 01_llm_testing_basics/source_materials/day1_first_request.py
python 01_llm_testing_basics/source_materials/day3_evaluator.py
npx promptfoo eval -c 01_llm_testing_basics/source_materials/day5_promptfoo.yaml

# Модуль 2: security testing
python 02_prompt_injection_and_security/source_materials/day8_prompt_injection.py
python 02_prompt_injection_and_security/source_materials/day10_guardrails.py
python 02_prompt_injection_and_security/source_materials/day12_regression_testing.py
```

## Финальный проект

Собрать мини AI QA framework: тест-план, AI test cases, security checks, hallucination checks и отчёт. Подробности в `final_project/README.md`.

## Безопасность

- Не публикуйте `.env` и API-ключи
- Security-задания — только для своих систем
- Не применяйте prompt injection к чужим сервисам
