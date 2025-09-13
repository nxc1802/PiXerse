"""
Chat session and message schemas
"""

from datetime import datetime
from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field, ConfigDict
from app.models.chat import MessageRole


class ChatSessionBase(BaseModel):
    session_token: str = Field(..., description="Session token")


class ChatSessionCreate(BaseModel):
    pass  # Session token will be generated automatically


class ChatSessionResponse(ChatSessionBase):
    session_id: int
    created_at: datetime
    last_activity_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class ChatMessageBase(BaseModel):
    role: MessageRole = Field(..., description="Message role (USER or ASSISTANT)")
    content: str = Field(..., min_length=1, description="Message content")


class ChatMessageCreate(ChatMessageBase):
    session_id: int = Field(..., description="Chat session ID")


class ChatMessageResponse(ChatMessageBase):
    message_id: int
    session_id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class ToolCallBase(BaseModel):
    tool_name: str = Field(..., min_length=1, max_length=100, description="Tool name")
    tool_input: Optional[Dict[str, Any]] = Field(None, description="Tool input parameters")
    tool_output: Optional[Dict[str, Any]] = Field(None, description="Tool output result")


class ToolCallCreate(ToolCallBase):
    message_id: int = Field(..., description="Chat message ID")


class ToolCallResponse(ToolCallBase):
    tool_call_id: int
    message_id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class ChatSessionDetailResponse(ChatSessionResponse):
    messages: List[ChatMessageResponse] = []

    model_config = ConfigDict(from_attributes=True)


class ChatMessageDetailResponse(ChatMessageResponse):
    tool_calls: List[ToolCallResponse] = []

    model_config = ConfigDict(from_attributes=True)


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="User message")
    session_token: Optional[str] = Field(None, description="Existing session token (optional)")


class ChatResponse(BaseModel):
    message: ChatMessageResponse
    session: ChatSessionResponse
    tool_calls: List[ToolCallResponse] = []
