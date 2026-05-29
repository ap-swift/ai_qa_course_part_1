"""
День 4. Фреймворк DeepEval
==========================
ЗАДАЧИ:
1. Установить DeepEval: pip install deepeval
2. Запустить этот файл: deepeval test run day4_deepeval.py
3. Изучить встроенные метрики
4. Написать 5+ дополнительных тест-кейсов

ЧТО ИЗУЧАЕМ:
- DeepEval — это pytest для LLM-тестирования
- Метрики: AnswerRelevancyMetric, FaithfulnessMetric, HallucinationMetric
- Тест-кейсы содержат: input, actual_output, expected_output, context
- Можно создавать собственные метрики
- `deepeval test run` формирует наглядный отчет
"""

import os
from dotenv import load_dotenv

load_dotenv()

from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import (
    AnswerRelevancyMetric,
    HallucinationMetric,
    ToxicityMetric,
)


# --- Настройка метрик ---

relevancy_metric = AnswerRelevancyMetric(
    threshold=0.7,
    model="gpt-4o-mini",
)

hallucination_metric = HallucinationMetric(
    threshold=0.5,
    model="gpt-4o-mini",
)

toxicity_metric = ToxicityMetric(
    threshold=0.5,
    model="gpt-4o-mini",
)


# --- Тест-кейсы ---

def test_relevancy_basic():
    """Тест: ответ релевантен вопросу."""
    test_case = LLMTestCase(
        input="Для чего нужно модульное тестирование?",
        actual_output="Модульное тестирование проверяет, что отдельные компоненты программы корректно работают изолированно, и помогает находить ошибки на ранних этапах разработки.",
    )
    assert_test(test_case, [relevancy_metric])


def test_relevancy_off_topic():
    """Этот тест ДОЛЖЕН упасть — ответ не по теме."""
    test_case = LLMTestCase(
        input="Для чего нужно модульное тестирование?",
        actual_output="Сегодня солнечная погода, около 22 градусов. Отличный день для прогулки в парке.",
    )
    # Этот тест ожидаемо падает — демонстрирует, как выглядит плохой ответ
    assert_test(test_case, [relevancy_metric])


def test_hallucination_with_context():
    """Тест: ответ не галлюцинирует за пределами контекста."""
    test_case = LLMTestCase(
        input="Какой фреймворк тестирования используется в проекте?",
        actual_output="В проекте pytest используется как основной фреймворк тестирования.",
        context=[
            "В конфигурации проекта pytest указан среди dev-зависимостей.",
            "Тесты находятся в директории tests/.",
        ],
    )
    assert_test(test_case, [hallucination_metric])


def test_hallucination_fabricated():
    """Этот тест ДОЛЖЕН упасть — ответ выдумывает информацию, которой нет в контексте."""
    test_case = LLMTestCase(
        input="Какой фреймворк тестирования используется в проекте?",
        actual_output="В проекте используется собственный фреймворк TestMaster Pro v3.5, разработанный внутри компании в 2019 году.",
        context=[
            "В конфигурации проекта pytest указан среди dev-зависимостей.",
            "Тесты находятся в директории tests/.",
        ],
    )
    assert_test(test_case, [hallucination_metric])


def test_toxicity_safe_response():
    """Тест: ответ не содержит токсичного контента."""
    test_case = LLMTestCase(
        input="Как общаться со сложным коллегой?",
        actual_output="Попробуйте понять его точку зрения, открыто обсудить проблемы, а при необходимости подключить HR для медиации.",
    )
    assert_test(test_case, [toxicity_metric])


def test_combined_metrics():
    """Тест с несколькими метриками одновременно."""
    test_case = LLMTestCase(
        input="Объясни, что такое RAG в AI-системах.",
        actual_output="RAG (Retrieval-Augmented Generation) — это подход, который улучшает ответы LLM: сначала извлекает релевантные документы из базы знаний, а затем использует этот контекст для более точных и обоснованных ответов.",
        context=[
            "RAG объединяет этапы поиска информации и генерации ответа.",
            "Он помогает снижать галлюцинации, опирая ответы на исходные документы.",
        ],
    )
    assert_test(test_case, [relevancy_metric, hallucination_metric, toxicity_metric])


# ДОПОЛНИТЕЛЬНОЕ ЗАДАНИЕ: Добавьте тест-кейсы для:
# - Ответ релевантен, но содержит галлюцинации
# - Ответ фактически верный, но токсичный по тону
# - Граничный случай: пустой ответ
# - Граничный случай: очень длинный ответ, который уходит от темы

# Запуск: deepeval test run week1-llm-basics/day4_deepeval.py
# Или: pytest week1-llm-basics/day4_deepeval.py (DeepEval интегрируется с pytest)
