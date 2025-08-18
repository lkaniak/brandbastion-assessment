from agno.team import Team

from src.agents import customer_success_agent, data_engineer_agent, social_media_data_analyst_agent
from agno.models.openai import OpenAIChat
from src.config import app_settings

reasoning_social_media_team = Team(
    name="Reasoning Social Media Team",
    mode="coordinate",
    members=[
        customer_success_agent,
        data_engineer_agent,
        social_media_data_analyst_agent,
    ],
    model=OpenAIChat(
        id="gpt-4o",
        api_key=app_settings.OPENAI_API_KEY,
        temperature=0.07,
    ),
    description="""You are a senior Social Media and Branding analyst. Given a user query and a set of reports and comments, you are tasked to
        help him to understand his query given the data available.""",
    enable_file_upload=True,
    instructions="""
    You are a senior Social Media and Branding analyst coordinating a team to help users understand their queries using available data.

    WORKFLOW:
    1. When files are uploaded, IMMEDIATELY delegate to the Data Engineer Agent to process the files using the process_uploaded_files tool, then create_analysis_context, and finally add_files_to_context.
    2. Ask the Customer Success Agent to understand the customer query.
    3. Ask the Data Analyst to help build a plan to answer the query.
    4. Ask the Data Engineer to provide all relevant information to achieve that plan.
    5. Correlate the plan with the information provided to check if it's possible to answer the question.
    6. Finally, build a report that answers the question and provide follow up questions to the customer.

    CRITICAL FILE HANDLING:
    - When files are uploaded, you MUST delegate to the Data Engineer Agent FIRST
    - The Data Engineer should use these tools in sequence:
      1. process_uploaded_files - to extract content from files
      2. create_analysis_context - to create structured context
      3. add_files_to_context - to add files to working context
    - Only after file processing is complete, proceed with the normal workflow

    ERROR HANDLING:
    - If any step fails, provide a friendly helpful message to the customer
    - Do not highlight where the error is coming from
    - If file processing fails, inform the user and ask them to try again
    """,
    enable_agentic_context=True,
    share_member_interactions=True,
    show_members_responses=True,
    debug_mode=True,
    debug_level=2,
    enable_file_upload=True,
)
