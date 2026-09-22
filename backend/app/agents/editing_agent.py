from __future__ import annotations

from pathlib import Path
from typing import Any

from app.agents.base_agent import BaseAgent
from app.services.artifact_versioning import ArtifactVersionManager


class ConversationalEditingAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(name='editing_agent', role='editing')

    def run(self, state: dict[str, Any] | str | None = None, **kwargs: Any) -> dict[str, Any]:
        if isinstance(state, dict):
            instruction = state.get('edit_instruction') or state.get('instruction') or ''
            state = dict(state)
        elif isinstance(state, str):
            instruction = state
            state = {'instruction': instruction}
        else:
            instruction = ''
            state = {}

        source_file = state.get('artifact_file') or state.get('source_file') or ''
        versioned = {}
        if source_file:
            manager = ArtifactVersionManager(base_dir=str(Path(source_file).parent))
            versioned = manager.apply_edit(source_file, instruction)

        state.update({
            'agent': self.name,
            'status': 'completed',
            'instruction': instruction,
            'artifact_file': versioned.get('file_path', source_file),
            'version': versioned.get('version', 'v1'),
            'edit_summary': (
                f"Created a new revision ({versioned.get('version', 'v1')}) after: {instruction}"
                if instruction and versioned
                else 'Updated the existing artifact while preserving tone, structure, and layout.'
            ),
        })
        return state
