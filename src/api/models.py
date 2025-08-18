from typing import Optional, Dict, Any
from pydantic import BaseModel


class Model(BaseModel):
    name: str
    model: str
    provider: str


class Agent(BaseModel):
    agent_id: str
    name: str
    description: str
    model: Model
    storage: Optional[bool] = False


class Team(BaseModel):
    team_id: str
    name: str
    description: str
    model: Model
    storage: Optional[bool] = False


class SessionEntry(BaseModel):
    session_id: str
    title: str
    created_at: int


class ChatMessage(BaseModel):
    role: str
    content: str
    created_at: int


class ToolCall(BaseModel):
    role: str
    content: Optional[str]
    tool_call_id: str
    tool_name: str
    tool_args: Dict[str, Any]
    tool_call_error: bool
    metrics: Dict[str, Any]
    created_at: int


class ChatEntry(BaseModel):
    message: ChatMessage
    response: Dict[str, Any]


class RunRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    stream: Optional[bool] = True


class RunResponse(BaseModel):
    content: Optional[str]
    content_type: str
    event: str
    run_id: Optional[str]
    agent_id: Optional[str]
    session_id: Optional[str]
    created_at: int


class StatusResponse(BaseModel):
    status: str
    version: str
