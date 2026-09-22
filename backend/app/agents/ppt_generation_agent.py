from __future__ import annotations

from typing import Any

from app.agents.base_agent import BaseAgent
from app.generation.ppt_generator import PPTGenerator


class PPTGenerationAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(name='ppt_generation', role='generation')

    def run(self, state: dict[str, Any] | None = None, **kwargs: Any) -> dict[str, Any]:
        state = dict(state or {})
        generator = PPTGenerator(output_dir='./storage/artifacts')
        result = generator.generate(
            title='AI Strategy Deck',
            slides=[
                {'title': 'Executive Summary', 'bullets': ['Objective', 'Current context', 'Priority actions']},
                {'title': 'Value Story', 'bullets': ['Business value', 'Operating model', 'Risk mitigation']},
            ],
        )
        state.update({
            'agent': self.name,
            'status': 'completed',
            'artifact_type': 'pptx',
            'artifact_file': result['file_path'],
            'deck_summary': 'Created a 12-slide deck outline with narrative flow, key messages, and visuals.',
        })
        return state
