# Модуль 0. Старт курса

## Цель модуля

Подготовить окружение и безопасно запустить первый пример без облачного API.

## Установка

```bash
cd stepik_course_package
python3 -m venv .venv
source .venv/bin/activate
pip install -r code/requirements.txt
cp .env.example .env
```

## Smoke test

```bash
python code/smoke_test_llm_provider.py
```

Ожидаемый результат:

```text
provider: mock
model: strict
response: Paris is the capital of France.
```

## Выбор LLM provider

По умолчанию используется `LLM_PROVIDER=mock`. Для реальных экспериментов:

- `ollama` — локальные модели без облачного API
- `gigachat` / `yandexgpt` — если доступны
- `openai_compatible` — любой совместимый endpoint

## Безопасность `.env`

- Не публикуйте `.env` и API-ключи
- Используйте `.env.example` как шаблон
- Если ключ случайно опубликован — сразу отзовите его

## Чек-лист

- [ ] Python-окружение создано
- [ ] Зависимости установлены
- [ ] `.env` создан локально
- [ ] Smoke test работает
