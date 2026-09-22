from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.models.chat import Artifact, Conversation, User
from app.schemas.chat import ChatRequest, ConversationCreate, TokenResponse, UserCreate, UserLogin
from app.services.auth import create_access_token, decode_token, hash_password, verify_password
from app.agents.orchestrator import MultiAgentOrchestrator
from app.services.chat_service import ChatService

api_router = APIRouter()
router = api_router
security = HTTPBearer()
settings = get_settings()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    try:
        payload = decode_token(credentials.credentials)
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except Exception as exc:  # pragma: no cover - authentication guard
        raise HTTPException(status_code=401, detail="Invalid token") from exc


@api_router.get("/health")
def api_health() -> dict[str, str]:
    return {"status": "ok"}


@api_router.post("/auth/register", response_model=TokenResponse)
def register_user(payload: UserCreate, db: Session = Depends(get_db)) -> TokenResponse:
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    user = User(
        email=payload.email,
        username=payload.username,
        hashed_password=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return TokenResponse(access_token=create_access_token(user.email))


@api_router.post("/auth/login", response_model=TokenResponse)
def login_user(payload: UserLogin, db: Session = Depends(get_db)) -> TokenResponse:
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return TokenResponse(access_token=create_access_token(user.email))


@api_router.get("/conversations")
def list_conversations(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> list[dict[str, Any]]:
    service = ChatService(db)
    conversations = service.list_conversations(current_user.id)
    return [
        {
            "id": c.id,
            "title": c.title,
            "created_at": c.created_at.isoformat(),
            "updated_at": c.updated_at.isoformat(),
        }
        for c in conversations
    ]


@api_router.get("/artifacts")
def list_artifacts(conversation_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> list[dict[str, Any]]:
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id, Conversation.user_id == current_user.id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    service = ChatService(db)
    artifacts = service.list_artifacts(conversation_id)
    return [
        {
            "id": artifact.id,
            "name": artifact.name,
            "artifact_type": artifact.artifact_type,
            "version": artifact.version,
            "status": artifact.status,
            "file_path": artifact.file_path,
            "created_at": artifact.created_at.isoformat(),
            "artifact_metadata": artifact.artifact_metadata,
        }
        for artifact in artifacts
    ]


@api_router.post("/conversations", response_model=dict[str, Any])
def create_conversation(payload: ConversationCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> dict[str, Any]:
    service = ChatService(db)
    conversation = service.create_conversation(current_user.id, payload.title)
    return {"id": conversation.id, "title": conversation.title}


@api_router.post("/chat")
def process_chat(payload: ChatRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> dict[str, Any]:
    service = ChatService(db)

    if payload.conversation_id is None:
        conversation = service.create_conversation(current_user.id, "New chat")
    else:
        conversation = db.query(Conversation).filter(Conversation.id == payload.conversation_id, Conversation.user_id == current_user.id).first()
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

    service.add_message(conversation.id, "user", payload.message)

    if payload.artifact_id is not None:
        artifact = db.query(Artifact).filter(Artifact.id == payload.artifact_id, Artifact.conversation_id == conversation.id).first()
        if not artifact:
            raise HTTPException(status_code=404, detail="Artifact not found")
        updated = service.apply_edit_to_artifact(artifact.id, payload.message)
        response_text = f"Updated {artifact.name} to {updated.version} with the requested edit."
        citations = [f"artifact://{updated.id}/{updated.version}"]
        service.add_message(conversation.id, "assistant", response_text, citations)
        return {
            "conversation_id": conversation.id,
            "assistant_reply": response_text,
            "citations": citations,
            "artifact_id": updated.id,
            "artifact_version": updated.version,
        }

    uploaded_files = [
        artifact.file_path
        for artifact in service.list_artifacts(conversation.id)
        if artifact.file_path and artifact.file_path.strip()
    ]

    orchestrator = MultiAgentOrchestrator()
    response = orchestrator.run(
        request=payload.message,
        conversation_id=conversation.id,
        uploaded_files=uploaded_files,
        user_context={"theme": "enterprise proposal"},
    )

    response_text = response.get('summary') or "The orchestration layer processed your request successfully."
    citations = response.get('citations') or ["demo://phase3/orchestrated-response"]
    service.add_message(conversation.id, "assistant", response_text, citations)

    return {
        "conversation_id": conversation.id,
        "assistant_reply": response_text,
        "citations": citations,
    }


@api_router.post("/upload")
def upload_file(
    conversation_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    service = ChatService(db)
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id, Conversation.user_id == current_user.id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    saved = service.save_uploaded_file(file, conversation_id, current_user.id)
    service.create_artifact(
        conversation.id,
        name=file.filename or "uploaded_file",
        artifact_type="uploaded_file",
        file_path=saved["file_path"],
        version="v1",
        status="uploaded",
        metadata={"size": saved["size"], "source": "upload"},
    )
    return {
        "message": "File uploaded successfully",
        "file_name": file.filename,
        "file_path": saved["file_path"],
        "conversation_id": conversation.id,
    }
