from __future__ import annotations

from typing import Any

from app.agents.base_agent import BaseAgent


class SupervisorAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(name='supervisor', role='orchestrator')

    def run(self, state: dict[str, Any] | str | None = None, request: str | None = None, **kwargs: Any) -> dict[str, Any]:
        if isinstance(state, dict):
            payload = dict(state)
            request = str(payload.get('request', request or ''))
        elif state is not None:
            payload = {'request': str(state)}
            request = str(state)
        else:
            payload = {}
            request = str(request or kwargs.get('request') or '')

        payload.setdefault('request', request)

        request_lower = request.lower()
        route = []

        if 'research' in request_lower or 'latest' in request_lower or 'trends' in request_lower:
            route.append('web_research')
        if 'proposal' in request_lower or 'report' in request_lower or 'document' in request_lower:
            route.append('document_analysis')
        if 'presentation' in request_lower or 'ppt' in request_lower or 'slides' in request_lower:
            route.append('ppt_analysis')
        if 'knowledge' in request_lower or 'enterprise' in request_lower or 'rag' in request_lower:
            route.append('enterprise_rag')

        if not route:
            route = ['document_analysis', 'enterprise_rag']

        payload.update({
            'agent': self.name,
            'role': self.role,
            'status': 'completed',
            'route': route,
            'request': request,
        })
        return payload
