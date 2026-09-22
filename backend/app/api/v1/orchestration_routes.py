from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.agents.orchestrator import MultiAgentOrchestrator
from app.api.v1.routes import get_current_user
from app.database import get_db
from app.models.chat import Conversation, User

orchestration_router = APIRouter()


class OrchestrationRequest(BaseModel):
    message: str
    conversation_id: int | None = None
    uploaded_files: list[str] | None = None
    user_context: dict[str, Any] | None = None
    edit_instruction: str | None = None
    artifact_id: int | None = None
    artifact_file: str | None = None


@orchestration_router.post("/orchestrate")
def orchestrate(req: OrchestrationRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> dict[str, Any]:
    conversation = None
    if req.conversation_id is not None:
        conversation = db.query(Conversation).filter(Conversation.id == req.conversation_id, Conversation.user_id == current_user.id).first()
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
    user_context = dict(req.user_context or {})
    if req.artifact_file:
        user_context['artifact_file'] = req.artifact_file
    if req.artifact_id is not None:
        user_context['artifact_id'] = req.artifact_id

    result = MultiAgentOrchestrator().run(
        request=req.message,
        conversation_id=req.conversation_id or (conversation.id if conversation else 0),
        uploaded_files=req.uploaded_files or [],
        user_context=user_context,
        edit_instruction=req.edit_instruction,
    )
    return {"message": "Orchestration completed", "result": result}
