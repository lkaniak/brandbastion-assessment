from agno.workflow.v2.step import Step, StepInput, StepOutput
from src.agents.data_analyst_agent import data_analyst_agent
from src.workflow.agent_message import AgentFinalResponse


def check_query_subject(step_input: StepInput) -> StepOutput:
    """
    Check if the query is about social media and media brand analysis.
    Also analyze the previous interaction to check context.
    """
    query = step_input.message
    if not query:
        return StepOutput(success=False, error="No query provided")

    try:
        response = data_analyst_agent.run(query)
    except Exception as e:
        return StepOutput(
            success=False,
            content=AgentFinalResponse(
                error_message="I could not understand your query, please try again."
            ),
            error=f"Error parsing query: {e}",
        )

    response_content = response.content
    if response_content.query_type == "analytical":
        return StepOutput(success=True, content=response_content)
    else:
        return StepOutput(
            success=False,
            content=AgentFinalResponse(final_answer=response_content.helpful_message),
            stop=True,
        )


check_query_subject_step = Step(
    name="Check Query Subject",
    description="Check if the query is about social media and media brand analysis.",
    executor=check_query_subject,
    max_retries=1,
)
