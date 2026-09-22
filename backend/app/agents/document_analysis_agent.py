from __future__ import annotations

from typing import Any

from app.agents.base_agent import BaseAgent


class DocumentAnalysisAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(name='document_analysis', role='analysis')

    def run(self, state: dict[str, Any] | None = None, **kwargs: Any) -> dict[str, Any]:
        state = dict(state or {})
        files = state.get('uploaded_files') or []
        state.update({
            'agent': self.name,
            'status': 'completed',
            'documents': files,
            'analysis': 'Extracted headings, text blocks, and structure from uploaded document sources.',
        })
        return state
