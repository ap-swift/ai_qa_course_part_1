# Provider-agnostic LLM clients

Эта папка содержит единый слой для работы с LLM в курсе. Курс обучает AI QA methodology, а не конкретному провайдеру, поэтому учебные примеры используют `get_llm_client()` и метод `generate(prompt)`.

## Как выбрать provider

В локальном `.env` укажите один режим:

```env
LLM_PROVIDER=mock
```

Доступные значения:

- `mock` — без API, работает сразу после установки зависимостей.
- `ollama` — локальная модель через Ollama.
- `gigachat` — точка интеграции для GigaChat по официальной документации.
- `yandexgpt` — точка интеграции для YandexGPT по официальной документации.
- `openai_compatible` — любой OpenAI-compatible endpoint, если он доступен вам юридически и технически.

## Mock

```bash
LLM_PROVIDER=mock python code/smoke_test_llm_provider.py
```

Mock возвращает предсказуемые ответы и подходит для первых уроков, автопроверки и проверки логики test suite без облачного API.

## Ollama

Установите Ollama и скачайте модель:

```bash
ollama serve
ollama pull qwen2.5:7b
```

В `.env`:

```env
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:7b
```

Проверка:

```bash
python code/smoke_test_llm_provider.py
```

## Cloud API

Для GigaChat/YandexGPT проверьте актуальные условия, регистрацию, оплату, лимиты и документацию провайдера самостоятельно. Курс не обещает, что конкретный сервис доступен всем студентам.

Для совместимых endpoints используйте:

```env
LLM_PROVIDER=openai_compatible
OPENAI_COMPATIBLE_BASE_URL=https://api.example.com/v1
OPENAI_COMPATIBLE_API_KEY=your_api_key_here
OPENAI_COMPATIBLE_MODEL=your_model_name_here
```

## Безопасность ключей

Не публикуйте `.env`, не вставляйте ключи в Stepik, GitHub, отчеты, комментарии и скриншоты. Если ключ случайно опубликован, сразу отзовите или перевыпустите его у провайдера.
