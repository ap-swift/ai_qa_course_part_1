"""Smoke test для выбранного LLM provider.

Скрипт не печатает API-ключи. Его можно безопасно использовать в первых
уроках и Stepik-отчетах, если не вставлять содержимое `.env`.
"""

from llm_clients.base import LLMClientError
from llm_clients.factory import get_llm_client


def main() -> None:
    try:
        client = get_llm_client()
        response = client.generate("Какая столица Франции? Ответь одним коротким предложением.")
    except NotImplementedError as exc:
        print("Provider настроен, но не реализован в шаблоне курса.")
        print(str(exc))
        return
    except LLMClientError as exc:
        print("Проверка LLM provider завершилась ошибкой.")
        print(str(exc))
        return

    print(f"provider: {client.provider_name}")
    print(f"model: {getattr(client, 'model_name', 'unknown')}")
    print(f"response: {response[:500]}")


if __name__ == "__main__":
    main()
