from typing import List, Optional
from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from fastapi.responses import StreamingResponse
from src.api.models import Agent, Team, SessionEntry, RunRequest, StatusResponse
from src.api.services import playground_service

playground_router = APIRouter(prefix="/v1/playground", tags=["playground"])

chat_router = APIRouter(tags=["legacy"])


@playground_router.get("/status", response_model=StatusResponse)
async def get_playground_status():
    """Get playground status"""
    return StatusResponse(status="healthy", version="1.0.0")


@chat_router.get("/health")
async def health_check():
    """health check endpoint"""
    return {"status": "healthy"}


@chat_router.post("/chat")
async def chat_endpoint(
    message: str = Form(...), files: Optional[List[UploadFile]] = File(None)
):
    """chat endpoint - redirects to team run"""
    try:
        file_data = []
        if files:
            for file in files:
                content = await file.read()
                file_info = {
                    "filename": file.filename,
                    "content_type": file.content_type,
                    "content": content,
                }
                file_data.append(file_info)

        request = RunRequest(message=message, stream=True)

        return StreamingResponse(
            playground_service.stream_response("social-media-team", request, file_data),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            },
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@playground_router.get("/agents", response_model=List[Agent])
async def get_playground_agents():
    """Get all available agents"""
    return playground_service.get_agents()


@playground_router.get("/agents/{agent_id}/sessions", response_model=List[SessionEntry])
async def get_agent_sessions(agent_id: str):
    """Get sessions for a specific agent"""
    return playground_service.get_agent_sessions(agent_id)


@playground_router.get("/agents/{agent_id}/sessions/{session_id}")
async def get_agent_session(agent_id: str, session_id: str):
    """Get a specific agent session"""
    session = playground_service.get_session(session_id)
    if not session or session.get("agent_id") != agent_id:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@playground_router.delete("/agents/{agent_id}/sessions/{session_id}")
async def delete_agent_session(agent_id: str, session_id: str):
    """Delete an agent session"""
    session = playground_service.get_session(session_id)
    if not session or session.get("agent_id") != agent_id:
        raise HTTPException(status_code=404, detail="Session not found")

    success = playground_service.delete_session(session_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete session")
    return {"message": "Session deleted successfully"}


@playground_router.get("/teams", response_model=List[Team])
async def get_playground_teams():
    """Get all available teams"""
    return playground_service.get_teams()


@playground_router.get("/teams/{team_id}/sessions", response_model=List[SessionEntry])
async def get_team_sessions(team_id: str):
    """Get sessions for a specific team"""
    return playground_service.get_team_sessions(team_id)


@playground_router.get("/teams/{team_id}/sessions/{session_id}")
async def get_team_session(team_id: str, session_id: str):
    """Get a specific team session"""
    session = playground_service.get_session(session_id)
    if not session or session.get("team_id") != team_id:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@playground_router.delete("/teams/{team_id}/sessions/{session_id}")
async def delete_team_session(team_id: str, session_id: str):
    """Delete a team session"""
    session = playground_service.get_session(session_id)
    if not session or session.get("team_id") != team_id:
        raise HTTPException(status_code=404, detail="Session not found")

    success = playground_service.delete_session(session_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete session")
    return {"message": "Session deleted successfully"}
