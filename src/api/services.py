import json
import asyncio
import uuid
from typing import List, Optional, Dict, Any, AsyncGenerator
from datetime import datetime
from src.orchestrator import social_media_analysis_workflow
from src.api.models import Agent, Team, SessionEntry, RunRequest
from agno.media import File

from src.workflow.agent_message import AgentFinalResponse
from src.config import app_settings


class PlaygroundService:
    def __init__(self):
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.agents: List[Agent] = []
        self.teams: List[Team] = []
        self._initialize_agents_and_teams()

    def _initialize_agents_and_teams(self):
        """Initialize the available agents and teams"""
        team = Team(
            team_id="social-media-team",
            name="Reasoning Social Media Team",
            description="A team of agents specialized in social media analysis and brand monitoring",
            model={"name": "gpt-4o", "model": "gpt-4o", "provider": "openai"},
            storage=True,
        )
        self.teams.append(team)

        # Create individual agents
        customer_agent = Agent(
            agent_id="customer-success-agent",
            name="Customer Success Agent",
            description="Specialized in understanding customer queries and providing support",
            model={"name": "gpt-4o", "model": "gpt-4o", "provider": "openai"},
            storage=True,
        )
        self.agents.append(customer_agent)

        data_engineer_agent = Agent(
            agent_id="data-engineer-agent",
            name="Data Engineer Agent",
            description="Specialized in processing and analyzing data files",
            model={"name": "gpt-4o", "model": "gpt-4o", "provider": "openai"},
            storage=True,
        )
        self.agents.append(data_engineer_agent)

        analyst_agent = Agent(
            agent_id="social-media-analyst-agent",
            name="Social Media Data Analyst Agent",
            description="Specialized in social media data analysis and insights",
            model={"name": "gpt-4o", "model": "gpt-4o", "provider": "openai"},
            storage=True,
        )
        self.agents.append(analyst_agent)

    def get_agents(self) -> List[Agent]:
        """Get all available agents"""
        return self.agents

    def get_teams(self) -> List[Team]:
        """Get all available teams"""
        return self.teams

    def get_agent_sessions(self, agent_id: str) -> List[SessionEntry]:
        """Get sessions for a specific agent"""
        sessions = []
        for session_id, session_data in self.sessions.items():
            if session_data.get("agent_id") == agent_id:
                sessions.append(
                    SessionEntry(
                        session_id=session_id,
                        title=session_data.get("title", "Untitled Session"),
                        created_at=session_data.get(
                            "created_at", int(datetime.now().timestamp())
                        ),
                    )
                )
        return sessions

    def get_team_sessions(self, team_id: str) -> List[SessionEntry]:
        """Get sessions for a specific team"""
        sessions = []
        for session_id, session_data in self.sessions.items():
            if session_data.get("team_id") == team_id:
                sessions.append(
                    SessionEntry(
                        session_id=session_id,
                        title=session_data.get("title", "Untitled Session"),
                        created_at=session_data.get(
                            "created_at", int(datetime.now().timestamp())
                        ),
                    )
                )
        return sessions

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific session by ID"""
        return self.sessions.get(session_id)

    def create_session(
        self, entity_id: str, entity_type: str, title: str = "New Session"
    ) -> str:
        """Create a new session"""
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            "session_id": session_id,
            "title": title,
            "created_at": int(datetime.now().timestamp()),
            "messages": [],
            f"{entity_type}_id": entity_id,
        }
        return session_id

    def delete_session(self, session_id: str) -> bool:
        """Delete a session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False

    async def stream_response(
        self, team_id: str, request: RunRequest, file_data: List[Dict] = None
    ) -> AsyncGenerator[str, None]:
        """Stream response from team execution"""
        try:
            files = None
            if file_data:
                files = []
                for file_obj in file_data:
                    files.append(
                        File(
                            name=file_obj["filename"],
                            content=file_obj["content"],
                            mime_type=file_obj["content_type"],
                        )
                    )

            workflow_response = await social_media_analysis_workflow.arun(
                message=request.message,
                additional_data={"files": files},
                session_id=app_settings.SESSION_ID,
                user_id=app_settings.USER_ID,
            )

            response_content = (
                workflow_response.content
                if workflow_response.content
                else AgentFinalResponse()
            )
            if isinstance(response_content, AgentFinalResponse):
                response_content = (
                    response_content.error_message or response_content.final_answer
                )
            else:
                response_content = str(response_content)

            chunk_size = 100
            for i in range(0, len(response_content), chunk_size):
                chunk = response_content[i : i + chunk_size]
                yield f"data: {json.dumps({'content': chunk, 'event': 'RunResponseContent'})}\n\n"
                await asyncio.sleep(0.01)

            yield f"data: {json.dumps({'event': 'RunCompleted', 'content': response_content})}\n\n"

        except Exception as e:
            error_data = {"event": "RunError", "content": str(e)}
            yield f"data: {json.dumps(error_data)}\n\n"


playground_service = PlaygroundService()
