from pydantic import BaseModel


class AgentFinalResponse(BaseModel):
    error_message: str = ""
    final_answer: str = ""
