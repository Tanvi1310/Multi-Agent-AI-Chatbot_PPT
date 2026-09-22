from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.database import get_db
from app.document_processing.analysis_service import AnalysisService
from app.models.chat import Conversation, User
from app.services.chat_service import ChatService
from app.api.v1.routes import get_current_user

analysis_router = APIRouter()


@analysis_router.post("/analyze")
def analyze_uploaded_file(
    conversation_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id, Conversation.user_id == current_user.id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    saved = ChatService(db).save_uploaded_file(file, conversation_id, current_user.id)
    analysis = AnalysisService().analyze_file(saved["file_path"])

    ChatService(db).create_artifact(
        conversation.id,
        name=file.filename or "analyzed_file",
        artifact_type="analysis",
        file_path=saved["file_path"],
        version="v1",
        status="analyzed",
        metadata={"analysis": analysis},
    )

    return {
        "conversation_id": conversation.id,
        "message": "File analyzed successfully.",
        "analysis": analysis,
    }
