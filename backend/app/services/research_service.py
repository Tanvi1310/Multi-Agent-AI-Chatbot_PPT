from __future__ import annotations

from typing import Any

from app.config import get_settings


class ResearchService:
    def __init__(self, provider: str = "mock") -> None:
        self.provider = provider

    def search(self, query: str, **kwargs: Any) -> dict[str, Any]:
        settings = get_settings()
        if self.provider == "serpapi" and settings.serpapi_api_key:
            return {
                'query': query,
                'results': [
                    {'title': 'SerpAPI enterprise AI research', 'url': 'https://serpapi.com'},
                ],
                'citations': ['https://serpapi.com'],
            }

        return {
            'query': query,
            'results': [
                {'title': 'Generative AI market outlook', 'url': 'https://example.com/research/generative-ai-trends'},
                {'title': 'Enterprise AI adoption', 'url': 'https://example.com/ai/2026-market-overview'},
            ],
            'citations': ['https://example.com/research/generative-ai-trends', 'https://example.com/ai/2026-market-overview'],
        }


class ResearchServiceFactory:
    @staticmethod
    def create(provider: str | None = None) -> ResearchService:
        settings = get_settings()
        chosen = (provider or settings.web_search_provider or 'mock').lower()
        return ResearchService(provider=chosen)
