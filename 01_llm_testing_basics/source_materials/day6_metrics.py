"""
Day 6: AI Error Types + Evaluation Metrics
============================================
ЗАДАЧИ:
1. Implement 3 custom metrics: BLEU-like, keyword overlap, semantic similarity
2. Compare your metrics with DeepEval's built-in metrics
3. Run both on the same test data
4. Analyze: when do they agree vs disagree?

ЧТО ИЗУЧАЕМ:
- BLEU: n-gram overlap between expected and actual (used in translation)
- ROUGE: recall-oriented, how much of reference is captured
- Cosine similarity: semantic closeness via embeddings
- Exact match: binary — either matches or doesn't
- Faithfulness: does the answer stick to provided context?
- Answer relevancy: does the answer address the question?
- Each metric has trade-offs: speed vs accuracy vs cost
"""

import os
import json
from collections import Counter
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# --- Custom Metrics Implementation ---

def bleu_score(reference: str, candidate: str, n: int = 1) -> float:
    """
    Simplified BLEU score (unigram precision).
    Measures: how many words in candidate appear in reference.
    """
    ref_tokens = reference.lower().split()
    cand_tokens = candidate.lower().split()

    if not cand_tokens:
        return 0.0

    ref_counts = Counter(ref_tokens)
    cand_counts = Counter(cand_tokens)

    clipped = {word: min(count, ref_counts.get(word, 0)) for word, count in cand_counts.items()}
    clipped_count = sum(clipped.values())

    return clipped_count / len(cand_tokens)


def rouge_l_score(reference: str, candidate: str) -> float:
    """
    Simplified ROUGE-L (Longest Common Subsequence based).
    Measures: how much of the reference is captured in candidate.
    """
    ref_tokens = reference.lower().split()
    cand_tokens = candidate.lower().split()

    if not ref_tokens or not cand_tokens:
        return 0.0

    # LCS using dynamic programming
    m, n = len(ref_tokens), len(cand_tokens)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if ref_tokens[i - 1] == cand_tokens[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    lcs_length = dp[m][n]
    recall = lcs_length / m
    precision = lcs_length / n
    if precision + recall == 0:
        return 0.0
    f1 = 2 * precision * recall / (precision + recall)
    return f1


def cosine_similarity_score(text1: str, text2: str) -> float:
    """
    Semantic similarity using OpenAI embeddings.
    This measures meaning, not just word overlap.
    """
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=[text1, text2],
    )
    emb1 = response.data[0].embedding
    emb2 = response.data[1].embedding

    dot_product = sum(a * b for a, b in zip(emb1, emb2))
    norm1 = sum(a * a for a in emb1) ** 0.5
    norm2 = sum(b * b for b in emb2) ** 0.5

    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot_product / (norm1 * norm2)


def keyword_overlap_score(reference: str, candidate: str) -> float:
    """Simple Jaccard similarity of unique words."""
    ref_words = set(reference.lower().split())
    cand_words = set(candidate.lower().split())
    if not ref_words or not cand_words:
        return 0.0
    intersection = ref_words & cand_words
    union = ref_words | cand_words
    return len(intersection) / len(union)


# --- Test Data ---

TEST_PAIRS = [
    {
        "name": "good_answer",
        "question": "What is unit testing?",
        "reference": "Unit testing is a software testing method where individual units or components are tested in isolation to verify they work correctly.",
        "candidate": "Unit testing is testing individual components of software in isolation to ensure they function correctly.",
    },
    {
        "name": "partial_answer",
        "question": "What is unit testing?",
        "reference": "Unit testing is a software testing method where individual units or components are tested in isolation to verify they work correctly.",
        "candidate": "Testing is important for software quality. There are many types of tests you can write.",
    },
    {
        "name": "hallucinated_answer",
        "question": "What is unit testing?",
        "reference": "Unit testing is a software testing method where individual units or components are tested in isolation to verify they work correctly.",
        "candidate": "Unit testing was invented by Kent Beck in 1847 as part of the Industrial Revolution to test steam engines.",
    },
    {
        "name": "off_topic",
        "question": "What is unit testing?",
        "reference": "Unit testing is a software testing method where individual units or components are tested in isolation to verify they work correctly.",
        "candidate": "The weather in Paris today is sunny with a high of 22 degrees Celsius.",
    },
    {
        "name": "verbose_but_correct",
        "question": "What is unit testing?",
        "reference": "Unit testing is a software testing method where individual units or components are tested in isolation to verify they work correctly.",
        "candidate": "Well, unit testing, you see, is essentially a methodology in software engineering where developers write small, focused tests that verify the behavior of individual units—typically functions or methods—in complete isolation from the rest of the system, ensuring correctness at the most granular level.",
    },
]


def evaluate_all_metrics(test_pairs: list[dict]) -> list[dict]:
    """Запустить все metrics на test pairs и сравнить."""
    results = []
    for pair in test_pairs:
        print(f"  Evaluating: {pair['name']}...")
        result = {
            "name": pair["name"],
            "bleu_1": round(bleu_score(pair["reference"], pair["candidate"]), 3),
            "rouge_l": round(rouge_l_score(pair["reference"], pair["candidate"]), 3),
            "cosine_sim": round(cosine_similarity_score(pair["reference"], pair["candidate"]), 3),
            "keyword_overlap": round(keyword_overlap_score(pair["reference"], pair["candidate"]), 3),
        }
        results.append(result)
    return results


if __name__ == "__main__":
    print("=== Day 6: Custom Metrics Evaluation ===\n")

    results = evaluate_all_metrics(TEST_PAIRS)

    # Display results as table
    print(f"\n{'Name':<22} {'BLEU-1':<8} {'ROUGE-L':<9} {'Cosine':<8} {'Keyword':<8}")
    print("-" * 58)
    for r in results:
        print(f"{r['name']:<22} {r['bleu_1']:<8} {r['rouge_l']:<9} {r['cosine_sim']:<8} {r['keyword_overlap']:<8}")

    # Analysis
    print("\n=== ANALYSIS ===")
    print("- BLEU: Measures word precision (are candidate words in reference?)")
    print("- ROUGE-L: Measures recall via longest common subsequence")
    print("- Cosine: Measures semantic meaning (expensive but smart)")
    print("- Keyword: Simple set overlap (fast but naive)")
    print("\nNotice how 'hallucinated_answer' might score OK on word overlap")
    print("but poorly on semantic similarity — that's why we need multiple metrics!")

    # Save results
    os.makedirs("week1-llm-basics/outputs", exist_ok=True)
    with open("week1-llm-basics/outputs/day6_metrics_results.json", "w") as f:
        json.dump(results, f, indent=2)

    # ДОПОЛНИТЕЛЬНОЕ ЗАДАНИЕ:
    # 1. Add BLEU-2 (bigram) metric
    # 2. Compare results: which metric is best at catching hallucinations?
    # 3. Run DeepEval's HallucinationMetric on the same data and compare
