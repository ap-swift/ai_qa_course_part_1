# Шаблон личного отчета по финальному проекту

Этот файл не нужно отправлять автору курса. Используйте его для самопроверки, GitHub README или портфолио.

## Ссылка на GitHub

Вставьте ссылку на публичный или приватный репозиторий, доступный преподавателю.

## Краткое описание проекта

Что за AI-система тестировалась: AI-бот, RAG-система, агент или demo workflow.

## Что тестировалось

- Качество LLM-ответов:
- Structured output / format:
- Prompt injection / jailbreak:
- Hallucinations:
- RAG retrieval, если применимо:
- Agent tools, если применимо:

## Какие баги найдены

Опишите 2-5 ключевых findings: steps, expected result, actual result, severity, evidence.

## Какие инструменты использованы

Например: `Python`, `pytest`, `promptfoo`, `DeepEval`, `ragas`, `LangChain`, `ChromaDB`, `GitHub Actions`.

## Как запустить проект

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
pytest tests -v
```

## Чему вы научились

Кратко опишите 3-5 навыков, которые вы отработали в проекте.

## Ограничения

Укажите, какие проверки не покрыты, какие данные синтетические и какие результаты требуют ручной валидации.
