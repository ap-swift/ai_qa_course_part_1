# Проект 1. LLM Test Suite

Комплексный набор автоматизированных проверок для оценки LLM-ответов в 5 категориях.

## Категории проверок

| Категория | Количество | Что проверяем |
|---|---:|---|
| Factuality | 7 | Модель сообщает корректные факты. |
| Format | 6 | Модель соблюдает требуемый формат ответа. |
| Safety | 6 | Модель корректно отказывает на опасные запросы. |
| Edge Cases | 7 | Модель устойчиво отвечает на необычные входные данные. |
| Hallucination | 4 | Модель не выдумывает неподтвержденную информацию. |

Всего: 30 test cases.

## Запуск

```bash
cd stepik_course_package
python 01_llm_testing_basics/projects/project1_llm_test_suite/run_suite.py
```

## Результаты

Скрипт формирует подробные результаты и summary report. Если создаются runtime-файлы в `outputs/`, не публикуйте их без проверки на секреты и приватные данные.

## Методика

- Deterministic checks: regex, keywords, format validation.
- LLM-as-a-judge: модель оценивает ответ по rubric, если подключен реальный provider.
- Scoring: оценка от 0.0 до 1.0, pass threshold обычно 0.7.

## Что описать в отчете

1. В каких категориях pass rate выше и ниже всего?
2. Какие failure patterns повторяются?
3. Как улучшить prompts, test data или guardrails?
4. Какой provider/model использовался? Не указывайте API-ключи.
