"""
День 6. Типы ошибок AI и метрики оценки
=========================================
ЗАДАЧИ:
1. Реализовать 3 метрики: BLEU-подобную, пересечение ключевых слов, семантическое сходство
2. Сравнить ваши метрики со встроенными метриками DeepEval
3. Запустить обе группы на одних и тех же тестовых данных
4. Проанализировать: когда метрики совпадают, а когда расходятся?

ЧТО ИЗУЧАЕМ:
- BLEU: пересечение n-грамм между ожидаемым и фактическим ответом (используется в переводе)
- ROUGE: ориентирован на recall — сколько из референса покрыто
- Cosine similarity: семантическая близость через эмбеддинги
- Exact match: бинарная проверка — совпадает или нет
- Faithfulness: придерживается ли ответ предоставленного контекста?
- Answer relevancy: отвечает ли ответ на заданный вопрос?
- У каждой метрики свои компромиссы: скорость vs точность vs стоимость
"""

import os
import json
from collections import Counter
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# --- Реализация метрик ---

def bleu_score(reference: str, candidate: str, n: int = 1) -> float:
    """
    Упрощённый BLEU score (unigram precision).
    Измеряет: какая доля слов candidate присутствует в reference.
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
    Упрощённый ROUGE-L (на основе наибольшей общей подпоследовательности).
    Измеряет: какая часть reference покрыта в candidate.
    """
    ref_tokens = reference.lower().split()
    cand_tokens = candidate.lower().split()

    if not ref_tokens or not cand_tokens:
        return 0.0

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
    Семантическое сходство через эмбеддинги OpenAI.
    Измеряет смысловую близость, а не просто пересечение слов.
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
    """Простое сходство Жаккара по уникальным словам."""
    ref_words = set(reference.lower().split())
    cand_words = set(candidate.lower().split())
    if not ref_words or not cand_words:
        return 0.0
    intersection = ref_words & cand_words
    union = ref_words | cand_words
    return len(intersection) / len(union)


# --- Тестовые данные ---

TEST_PAIRS = [
    {
        "name": "good_answer",
        "question": "Что такое модульное тестирование?",
        "reference": "Модульное тестирование — это метод тестирования ПО, при котором отдельные модули или компоненты проверяются изолированно, чтобы убедиться, что они работают корректно.",
        "candidate": "Модульное тестирование проверяет отдельные компоненты программы изолированно, чтобы убедиться в их корректной работе.",
    },
    {
        "name": "partial_answer",
        "question": "Что такое модульное тестирование?",
        "reference": "Модульное тестирование — это метод тестирования ПО, при котором отдельные модули или компоненты проверяются изолированно, чтобы убедиться, что они работают корректно.",
        "candidate": "Тестирование важно для качества ПО. Есть много разных видов тестов, которые можно писать.",
    },
    {
        "name": "hallucinated_answer",
        "question": "Что такое модульное тестирование?",
        "reference": "Модульное тестирование — это метод тестирования ПО, при котором отдельные модули или компоненты проверяются изолированно, чтобы убедиться, что они работают корректно.",
        "candidate": "Модульное тестирование придумал Кент Бек в 1847 году во время промышленной революции для проверки паровых двигателей.",
    },
    {
        "name": "off_topic",
        "question": "Что такое модульное тестирование?",
        "reference": "Модульное тестирование — это метод тестирования ПО, при котором отдельные модули или компоненты проверяются изолированно, чтобы убедиться, что они работают корректно.",
        "candidate": "Сегодня в Париже солнечная погода, температура поднимается до 22 градусов.",
    },
    {
        "name": "verbose_but_correct",
        "question": "Что такое модульное тестирование?",
        "reference": "Модульное тестирование — это метод тестирования ПО, при котором отдельные модули или компоненты проверяются изолированно, чтобы убедиться, что они работают корректно.",
        "candidate": "Модульное тестирование, по сути, является методикой разработки ПО, при которой разработчики пишут небольшие сфокусированные тесты для проверки поведения отдельных единиц кода — обычно функций или методов — в полной изоляции от остальной системы, чтобы убедиться в корректности на самом детальном уровне.",
    },
]


def evaluate_all_metrics(test_pairs: list[dict]) -> list[dict]:
    """Запустить все метрики на тестовых парах и сравнить."""
    results = []
    for pair in test_pairs:
        print(f"  Оценка: {pair['name']}...")
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
    print("=== День 6: Оценка метриками ===\n")

    results = evaluate_all_metrics(TEST_PAIRS)

    print(f"\n{'Название':<22} {'BLEU-1':<8} {'ROUGE-L':<9} {'Cosine':<8} {'Keyword':<8}")
    print("-" * 58)
    for r in results:
        print(f"{r['name']:<22} {r['bleu_1']:<8} {r['rouge_l']:<9} {r['cosine_sim']:<8} {r['keyword_overlap']:<8}")

    # Анализ
    print("\n=== АНАЛИЗ ===")
    print("- BLEU: Измеряет precision по словам (есть ли слова candidate в reference?)")
    print("- ROUGE-L: Измеряет recall через наибольшую общую подпоследовательность")
    print("- Cosine: Измеряет семантический смысл (дорого, но точно)")
    print("- Keyword: Простое пересечение множеств (быстро, но наивно)")
    print("\nОбратите внимание: 'hallucinated_answer' может получить ОК по пересечению слов,")
    print("но плохо по семантическому сходству — поэтому нужно несколько метрик!")

    # Сохранение результатов
    os.makedirs("week1-llm-basics/outputs", exist_ok=True)
    with open("week1-llm-basics/outputs/day6_metrics_results.json", "w") as f:
        json.dump(results, f, indent=2)

    # ДОПОЛНИТЕЛЬНОЕ ЗАДАНИЕ:
    # 1. Добавить метрику BLEU-2 (биграммы)
    # 2. Сравнить результаты: какая метрика лучше всего ловит галлюцинации?
    # 3. Запустить HallucinationMetric из DeepEval на тех же данных и сравнить
