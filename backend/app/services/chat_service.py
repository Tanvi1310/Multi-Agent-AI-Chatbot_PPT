from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models.chat import Artifact, Conversation, Message
from app.services.artifact_versioning import ArtifactVersionManager
from app.services.storage import ensure_storage_dirs


class ChatService:
    def __init__(self, db: Session):
        self.db = db

    def create_conversation(self, user_id: int, title: str = "New chat") -> Conversation:
        conversation = Conversation(user_id=user_id, title=title)
        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)
        return conversation

    def add_message(self, conversation_id: int, role: str, content: str, cited_sources: list[str] | None = None) -> Message:
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            cited_sources=json.dumps(cited_sources) if cited_sources else None,
        )
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message

    def list_conversations(self, user_id: int) -> list[Conversation]:
        return self.db.query(Conversation).filter(Conversation.user_id == user_id).order_by(Conversation.updated_at.desc()).all()

    def list_artifacts(self, conversation_id: int) -> list[Artifact]:
        return self.db.query(Artifact).filter(Artifact.conversation_id == conversation_id).order_by(Artifact.created_at.desc()).all()

    def create_artifact(self, conversation_id: int, *, name: str, artifact_type: str, file_path: str, version: str = "v1", status: str = "draft", metadata: dict[str, Any] | None = None) -> Artifact:
        artifact = Artifact(
            conversation_id=conversation_id,
            name=name,
            artifact_type=artifact_type,
            version=version,
            file_path=file_path,
            status=status,
            artifact_metadata=json.dumps(metadata) if metadata else None,
        )
        self.db.add(artifact)
        self.db.commit()
        self.db.refresh(artifact)
        return artifact

    def apply_edit_to_artifact(self, artifact_id: int, instruction: str) -> Artifact:
        artifact = self.db.query(Artifact).filter(Artifact.id == artifact_id).first()
        if not artifact:
            raise ValueError(f"Artifact {artifact_id} not found")

        manager = ArtifactVersionManager(base_dir=str(Path(artifact.file_path).parent))
        result = manager.apply_edit(artifact.file_path, instruction)

        updated = Artifact(
            conversation_id=artifact.conversation_id,
            name=Path(result['file_path']).name,
            artifact_type=artifact.artifact_type,
            version=result['version'],
            file_path=result['file_path'],
            status='draft',
            artifact_metadata=json.dumps({
                'source_artifact_id': artifact.id,
                'instruction': instruction,
                'previous_version': artifact.version,
            }),
        )
        self.db.add(updated)
        self.db.commit()
        self.db.refresh(updated)
        return updated

    def save_uploaded_file(self, upload: UploadFile, conversation_id: int, user_id: int) -> dict[str, Any]:
        ensure_storage_dirs()
        target_dir = Path("./storage/uploads") / str(user_id) / str(conversation_id)
        target_dir.mkdir(parents=True, exist_ok=True)
        file_name = upload.filename or "uploaded_file"
        safe_name = file_name.replace(" ", "_")
        destination = target_dir / safe_name
        content = upload.file.read()
        destination.write_bytes(content)
        return {"file_name": file_name, "file_path": str(destination), "size": len(content)}
