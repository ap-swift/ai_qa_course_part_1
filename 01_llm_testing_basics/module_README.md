# Модуль 1. Основы тестирования LLM

## Цель

Превратить субъективную оценку LLM-ответов в воспроизводимые тесты. Первые задания можно пройти с `LLM_PROVIDER=mock`.

## Уроки

- Первый provider-agnostic LLM-запрос
- Structured outputs и JSON validation
- Custom evaluator
- DeepEval и hallucination checks
- Promptfoo regression testing
- Базовые метрики качества (BLEU, ROUGE, cosine similarity)

## Файлы

```
source_materials/
  day1_first_request.py
  day2_structured_outputs.py
  day3_evaluator.py
  day4_deepeval.py
  day5_promptfoo_guide.py
  day5_promptfoo.yaml
  day6_metrics.py
projects/
  project1_llm_test_suite/
```

## Запуск

```bash
python source_materials/day1_first_request.py
python source_materials/day3_evaluator.py
npx promptfoo eval -c source_materials/day5_promptfoo.yaml
python projects/project1_llm_test_suite/run_suite.py
```

## Домашнее задание

Добавьте 10 тест-кейсов для выбранного AI-бота и опишите expected result для каждого.
