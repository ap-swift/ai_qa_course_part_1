"""Provider-neutral smoke test.

По умолчанию используется `LLM_PROVIDER=mock`, поэтому файл работает без API-ключей.
"""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from llm_clients.factory import get_llm_client


if __name__ == "__main__":
    client = get_llm_client()
    response = client.generate("Верни короткий JSON-статус для smoke test AI QA.")
    print(f"Provider: {client.provider_name}")
    print(f"Model: {getattr(client, 'model_name', 'unknown')}")
    print(f"Response: {response}")
