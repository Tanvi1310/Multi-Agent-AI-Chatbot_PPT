from __future__ import annotations

from typing import Any

from app.agents.base_agent import BaseAgent
from app.services.research_service import ResearchServiceFactory


class WebResearchAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(name='web_research', role='research')

    def run(self, state: dict[str, Any] | str, **kwargs: Any) -> dict[str, Any]:
        if isinstance(state, dict):
            request = str(state.get('request', ''))
            state = dict(state)
        else:
            request = str(state)
            state = {'request': request}

        service = ResearchServiceFactory.create()
        search_response = service.search(request)

        state.update({
            'agent': self.name,
            'status': 'completed',
            'research': f"Latest web research for '{request}' using a live-style provider with source URLs and citations.",
            'results': search_response.get('results', []),
            'citations': search_response.get('citations', []),
        })
        return state
