from __future__ import annotations

from typing import Any

from app.agents.base_agent import BaseAgent
from app.generation.document_generator import DocumentGenerator


class DocumentGenerationAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(name='document_generation', role='generation')

    def run(self, state: dict[str, Any] | None = None, **kwargs: Any) -> dict[str, Any]:
        state = dict(state or {})
        generator = DocumentGenerator(output_dir='./storage/artifacts')
        result = generator.generate(
            title=state.get('request', 'Generated Proposal').split('create a')[-1].strip().title() or 'Generated Proposal',
            sections=['Executive Summary', 'Market Opportunity', 'Implementation Plan'],
            body=state.get('retrieved_context', 'This proposal consolidates research and enterprise guidance for stakeholder-ready delivery.')
        )
        state.update({
            'agent': self.name,
            'status': 'completed',
            'artifact_type': 'docx',
            'artifact_file': result['file_path'],
            'draft_summary': 'Generated a proposal draft with executive summary, market analysis, and pricing narrative.',
        })
        return state
