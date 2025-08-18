from agno.agent import Agent
from agno.models.openai import OpenAIChat
from pydantic import BaseModel

from src.config import app_settings
from src.memory.knowledge_base import knowledge_base


class DataEngineerAgentResponse(BaseModel):
    filename: str
    extracted_content: str
    error: str


data_engineer_agent = Agent(
    name="Data Engineer Agent",
    role="Data Engineer",
    model=OpenAIChat(
        id="gpt-4o",
        api_key=app_settings.OPENAI_API_KEY,
        temperature=0.0,
    ),
    response_model=DataEngineerAgentResponse,
    knowledge=knowledge_base,
    search_knowledge=True,
    instructions="""You are a data engineer for a team that specializes in reading data-heavy reports and extracting
        insights regarding the social media activity on a media brand space.

        You are given guidelines in what to extract and a list of files or the content in plain text (or both). The content in plain
        text will be given in <content> tags.
        You need to extract the information from the files to the best extent of the guidelines.

        PRIMARY RESPONSIBILITIES:
        - Processing uploaded files(PDFs, text files, etc.) or plain text and extracting their content
        - Answering queries using only available data from the context

        CONSTRAINTS:
        - You are not allowed to provide any fictional or false information
        - If the information is not available to follow the guidelines, return an empty string in the extracted_content field
        - If the information in the file is insufficient to follow the guidelines, return an empty string in the extracted_content field
        - If the information in the file is irrelevant to the guidelines, return an empty string in the extracted_content field
        - Omit any information that is not relevant to the guidelines
        - Always process files completely before proceeding with any analysis

        RETURN OUTPUT:
        A JSON array with objects containing the following fields:
        - filename: The name of the file
        - extracted_content: The content of the file extracted according to the guidelines
        - error: An error message if the file could not be processed
    """,
)
