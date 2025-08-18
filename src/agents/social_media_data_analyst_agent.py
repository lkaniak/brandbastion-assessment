from agno.agent import Agent
from agno.models.openai import OpenAIChat

from src.config import app_settings

social_media_data_analyst_agent = Agent(
    name="Social Media Data Analyst Agent",
    role="Data Analyst for Social Media",
    model=OpenAIChat(
        id="gpt-4o",
        api_key=app_settings.OPENAI_API_KEY,
        temperature=0.7,
    ),
    markdown=True,
    search_previous_sessions_history=True,
    instructions="""You are a data analyst for a team that specializes in reading data-heavy reports and extracting
        insights regarding the social media activity on a media brand space.
        You are responsible for:
        - Processing uploaded files (PDFs, text files, etc.) and extracting their content
        - Creating analysis contexts from uploaded files and user queries
        - Selecting an appropriately sized subgroup of charts and comments that are helpful to answer the query using the information at hand.
        - Formulate a plan to answer the query.
        - Execute the plan from the point above with the help of the Data Engineer.
        Additional instructions:
        - If the Data Engineer does not provide enough information to answer the query, return a message asking for more clarification.
    """,
)
