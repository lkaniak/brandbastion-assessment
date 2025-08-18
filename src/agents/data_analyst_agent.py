from agno.agent import Agent
from agno.models.openai import OpenAIChat
from pydantic import BaseModel
from src.config import app_settings


class DataAnalystAgentResponse(BaseModel):
    query_type: str
    query_content: str
    helpful_message: str
    information_extract_guidelines: str


data_analyst_agent = Agent(
    name="Data Analyst Agent",
    role="Data Analyst",
    add_history_to_messages=True,
    num_history_runs=3,
    read_chat_history=True,
    debug_level=2,
    debug_mode=True,
    response_model=DataAnalystAgentResponse,
    parser_model=OpenAIChat(
        id="gpt-4o-mini",
        api_key=app_settings.OPENAI_API_KEY,
        temperature=0.3,
    ),
    instructions="""You are a friendly data analyst agent for a team that specializes in reading data-heavy reports and extracting
        insights regarding the social media activity on a media brand space.

        - Your role is to understand the customer query and identify if it is analytical in nature.
        - You also help translating output in a friendly manner.
        - You are allowed to query the chat history to understand the context of the conversation.
        - You are not allowed to answer any questions that are not related to social media and media brand analysis. If the query is not related,
        you should politely decline to help and re-steer the conversation to be about analytics or follow up on analytics.
        - In case the query is analytical, return some guidance on how to extract information from the extra content.

        RETURN OUTPUT:
        A JSON object with the following fields:
        - query_type: "analytical" or "other"
        - query_content: The content of the query
        - helpful_message: A message to the user to help them understand the query and the output.
        - information_extract_guidelines: A list of guidelines to extract information from the extra content if the query is analytical.
        Empty string if its other query type.
    """,
)
