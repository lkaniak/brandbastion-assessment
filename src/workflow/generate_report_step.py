from agno.workflow.v2.step import Step, StepInput, StepOutput
from src.agents.data_scientist_agent import data_scientist_agent
from src.workflow.agent_message import AgentFinalResponse


def generate_report(step_input: StepInput) -> StepOutput:
    """
    Generate a report based on the data at hand.
    """
    previous_step_content = step_input.previous_step_content
    if not previous_step_content or not previous_step_content.content_extracted:
        return StepOutput(
            success=False,
            content=AgentFinalResponse(
                error_message="""I could not find any data relevant to your query.
                Could you provide some data in which I can help you with?."""
            ),
            error="No data to generate a report from",
            stop=True,
        )

    try:
        response = data_scientist_agent.run(
            f"""
            You are given a list of data.
            You need to generate a report based on the data.

            DATA:
            {previous_step_content.content_extracted}

            QUERY:
            {step_input.message}
            """
        )

    except Exception as e:
        return StepOutput(
            success=False,
            content=AgentFinalResponse(error_message=f"An error has occurred: {e}"),
            error=f"An error has occurred: {e}",
            stop=True,
        )

    if not response or not response.content:
        return StepOutput(
            success=False,
            content=AgentFinalResponse(
                error_message="I could not generate a report based on the data at hand. Try again later."
            ),
            error="I could not generate a report based on the data at hand.",
            stop=True,
        )

    return StepOutput(
        success=True, content=AgentFinalResponse(final_answer=response.content)
    )


generate_report_step = Step(
    name="Generate Report",
    description="Generate a report based on the data at hand.",
    executor=generate_report,
    max_retries=1,
)
