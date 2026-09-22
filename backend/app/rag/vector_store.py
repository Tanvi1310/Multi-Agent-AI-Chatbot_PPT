from __future__ import annotations

from typing import Any

from app.config import get_settings


class MockVectorStore:
    def __init__(self, **kwargs: Any) -> None:
        self.kwargs = kwargs

    def similarity_search(self, query: str, k: int = 3) -> list[dict[str, Any]]:
        return [
            {'content': 'Enterprise AI strategy prioritizes data governance, executive storytelling, and phased modernization.', 'source': 'internal://enterprise-ai-strategy'},
            {'content': 'Proposal templates should preserve tone, structure, and emphasis on ROI and competitive positioning.', 'source': 'internal://proposal-template-guidance'},
        ][:k]


class PineconeVectorStore:
    def __init__(self, api_key: str | None = None, environment: str | None = None, index_name: str | None = None, **kwargs: Any) -> None:
        self.api_key = api_key
        self.environment = environment
        self.index_name = index_name
        self.kwargs = kwargs
        self._client = None

        try:
            from pinecone import Pinecone  # type: ignore
            if api_key:
                self._client = Pinecone(api_key=api_key, environment=environment or "us-east-1")
        except Exception:
            self._client = None

    def similarity_search(self, query: str, k: int = 3) -> list[dict[str, Any]]:
        if self._client is None:
            return MockVectorStore().similarity_search(query, k=k)

        index = self._client.Index(self.index_name or 'enterprise-rag')
        response = index.query(vector=[0.0] * 3, top_k=k, include_metadata=True, input_text=query)
        matches = []
        for item in response.get('matches', []):
            metadata = item.get('metadata', {})
            matches.append({'content': metadata.get('text', ''), 'source': metadata.get('source', 'internal://vector-store')})
        if matches:
            return matches
        return MockVectorStore().similarity_search(query, k=k)


class VectorStoreFactory:
    @staticmethod
    def create(provider: str | None = None, **kwargs: Any):
        settings = get_settings()
        chosen = (provider or settings.vector_db_provider or 'mock').lower()
        if chosen == 'pinecone':
            return PineconeVectorStore(
                api_key=settings.pinecone_api_key,
                environment=settings.pinecone_environment,
                index_name=settings.pinecone_index_name,
                **kwargs,
            )
        return MockVectorStore(**kwargs)
