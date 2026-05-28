"""Compatibility-wrapper вокруг provider-agnostic пакета llm_clients."""

from dataclasses import dataclass
from typing import Any

from llm_clients.base import LLMClientError
from llm_clients.factory import get_llm_client


@dataclass
class LLMResponse:
    text: str
    provider: str
    model: str
    raw: dict[str, Any] | None = None


class CourseLLMClient:
    """Compatibility adapter. В новом коде курса используйте `llm_clients.factory`."""

    def __init__(self) -> None:
        self._client = get_llm_client()
        self.provider = self._client.provider_name

    def chat(self, prompt: str, system: str = "You are a helpful AI QA assistant.") -> LLMResponse:
        full_prompt = f"System instruction: {system}\n\nUser prompt: {prompt}" if system else prompt
        text = self._client.generate(full_prompt)
        return LLMResponse(
            text=text,
            provider=self._client.provider_name,
            model=getattr(self._client, "model_name", "unknown"),
        )


if __name__ == "__main__":
    client = CourseLLMClient()
    response = client.chat("Return a short JSON status for an AI QA smoke test.")
    print(f"provider={response.provider} model={response.model}")
    print(response.text)
