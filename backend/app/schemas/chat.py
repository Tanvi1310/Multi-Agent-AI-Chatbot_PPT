from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    email: str
    username: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class MessageCreate(BaseModel):
    role: str = Field(default="user")
    content: str


class ConversationCreate(BaseModel):
    title: str = "New chat"


class ChatMessage(BaseModel):
    role: str
    content: str
    cited_sources: Optional[list[str]] = None


class ArtifactResult(BaseModel):
    id: int
    name: str
    artifact_type: str
    version: str
    file_path: str
    status: str
    artifact_metadata: Optional[str] = None


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None
    artifact_id: Optional[int] = None
