from __future__ import annotations

from typing import Any

from app.agents.base_agent import BaseAgent
from app.rag.vector_store import VectorStoreFactory


class EnterpriseRAGAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(name='enterprise_rag', role='retrieval')

    def run(self, state: dict[str, Any] | str, **kwargs: Any) -> dict[str, Any]:
        if isinstance(state, dict):
            request = str(state.get('request', ''))
            state = dict(state)
        else:
            request = str(state)
            state = {'request': request}

        store = VectorStoreFactory.create()
        matches = store.similarity_search(request, k=2)
        context = ' '.join(match.get('content', '') for match in matches if match.get('content'))

        state.update({
            'agent': self.name,
            'status': 'completed',
            'retrieved_context': context or 'Internal knowledge base matches: enterprise AI strategy, executive narrative, modernization themes.',
            'citations': [match.get('source', 'internal://enterprise-rag') for match in matches if match.get('source')],
        })
        return state
