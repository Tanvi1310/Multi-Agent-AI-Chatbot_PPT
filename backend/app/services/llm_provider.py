from __future__ import annotations

from typing import Any


class MockLLMProvider:
    def __init__(self, **kwargs: Any) -> None:
        self.kwargs = kwargs

    def complete(self, prompt: str, **kwargs: Any) -> str:
        return (
            "Structured proposal drafted with executive summary, strategic analysis, and a concise presentation outline "
            "aligned to the uploaded template and enterprise style."
        )


class LLMProviderFactory:
    @staticmethod
    def create(**kwargs: Any) -> MockLLMProvider:
        return MockLLMProvider(**kwargs)
