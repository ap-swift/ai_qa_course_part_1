# Финальный проект: AI QA для LLM-бота

## Цель

Собрать воспроизводимый набор AI QA-проверок, который показывает ваш подход к тестированию LLM-системы.

## Что можно тестировать

- FAQ-бот на mock, Ollama или доступном LLM API
- Любой AI-чатбот, к которому у вас есть доступ
- Учебный бот из материалов курса

## Обязательные элементы

- Test plan: scope, risks, tools, test data
- AI test cases: factuality, format, consistency, edge cases
- Prompt injection tests: direct injection, jailbreak, indirect injection
- Hallucination checks
- Automated run через `pytest` или `promptfoo`
- Отчёт о найденных дефектах с severity
- Рекомендации по улучшению
- README с командами запуска

## Рекомендуемая структура

```
ai-qa-project/
  README.md
  test_plan.md
  requirements.txt
  .env.example
  tests/
  configs/
  reports/
```

## Минимальный объём

- 15+ AI test cases
- 8+ security/prompt injection cases
- 5+ hallucination checks
- 1 команда для запуска
- 1 summary report

## Провайдер

Укажите в README, какой provider использовали. Не публикуйте `.env` и API-ключи.

## Самопроверка

Заполните `submission_template.md` и проверьте проект по `evaluation_rubric.md`.
