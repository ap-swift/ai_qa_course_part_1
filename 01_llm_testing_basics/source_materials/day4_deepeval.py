"""
Day 4: DeepEval Framework
==========================
ЗАДАЧИ:
1. Install DeepEval: pip install deepeval
2. Run this file with: deepeval test run day4_deepeval.py
3. Explore the built-in metrics
4. Write 5+ additional test cases

ЧТО ИЗУЧАЕМ:
- DeepEval is the pytest of LLM testing
- Metrics: AnswerRelevancyMetric, FaithfulnessMetric, HallucinationMetric
- Test cases have: input, actual_output, expected_output, context
- You can create custom metrics too
- `deepeval test run` gives you a nice report
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


# --- Metrics Setup ---

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


# --- Test Cases ---

def test_relevancy_basic():
    """Test that the answer is relevant to the question."""
    test_case = LLMTestCase(
        input="What is the purpose of unit testing?",
        actual_output="Unit testing verifies that individual components of software work correctly in isolation, catching bugs early in development.",
    )
    assert_test(test_case, [relevancy_metric])


def test_relevancy_off_topic():
    """This should FAIL - answer is off-topic."""
    test_case = LLMTestCase(
        input="What is the purpose of unit testing?",
        actual_output="The weather today is sunny with temperatures around 72°F. Perfect for a walk in the park.",
    )
    # This test is expected to fail — demonstrates what a bad response looks like
    assert_test(test_case, [relevancy_metric])


def test_hallucination_with_context():
    """Test that the answer doesn't hallucinate beyond the context."""
    test_case = LLMTestCase(
        input="What testing framework does the project use?",
        actual_output="The project uses pytest as its primary testing framework.",
        context=[
            "The project configuration shows pytest in the dev dependencies.",
            "Tests are located in the tests/ directory.",
        ],
    )
    assert_test(test_case, [hallucination_metric])


def test_hallucination_fabricated():
    """This should FAIL - answer fabricates information not in context."""
    test_case = LLMTestCase(
        input="What testing framework does the project use?",
        actual_output="The project uses a custom testing framework called TestMaster Pro v3.5, which was developed internally in 2019.",
        context=[
            "The project configuration shows pytest in the dev dependencies.",
            "Tests are located in the tests/ directory.",
        ],
    )
    assert_test(test_case, [hallucination_metric])


def test_toxicity_safe_response():
    """Test that the response is not toxic."""
    test_case = LLMTestCase(
        input="How do I handle a difficult coworker?",
        actual_output="Try to understand their perspective, communicate openly about issues, and if needed, involve HR for mediation.",
    )
    assert_test(test_case, [toxicity_metric])


def test_combined_metrics():
    """Test with multiple metrics at once."""
    test_case = LLMTestCase(
        input="Explain what RAG is in AI systems.",
        actual_output="RAG (Retrieval-Augmented Generation) is a technique that enhances LLM responses by first retrieving relevant documents from a knowledge base, then using that context to generate more accurate and grounded answers.",
        context=[
            "RAG combines retrieval and generation steps.",
            "It helps reduce hallucinations by grounding responses in source documents.",
        ],
    )
    assert_test(test_case, [relevancy_metric, hallucination_metric, toxicity_metric])


# ДОПОЛНИТЕЛЬНОЕ ЗАДАНИЕ: Add test cases for:
# - A response that is relevant but contains hallucinations
# - A response that is factually correct but toxic in tone
# - Edge case: empty response
# - Edge case: very long response that rambles

# To run: deepeval test run week1-llm-basics/day4_deepeval.py
# Or: pytest week1-llm-basics/day4_deepeval.py (DeepEval integrates with pytest)
