from agno.workflow.v2.step import Step, StepInput, StepOutput
from pydantic import BaseModel
from typing import List
from src.agents.data_engineer_agent import data_engineer_agent
from src.workflow.agent_message import AgentFinalResponse


class DataContextOutput(BaseModel):
    content_extracted: List[str]


def gather_data_from_context(step_input: StepInput) -> StepOutput:
    """
    Gather data from the context to help provide a better answer to the query.
    """
    previous_step_content = step_input.previous_step_content

    if (
        not previous_step_content
        or not previous_step_content.information_extract_guidelines
    ):
        return StepOutput(
            success=False,
            content=AgentFinalResponse(
                error_message="An error has occurred, please try again."
            ),
            error="No guidelines to extract information from the context",
            stop=True,
        )

    files = step_input.additional_data.get("files", None)
    if not files:
        return StepOutput(
            success=False,
            content=AgentFinalResponse(
                error_message="Please provide the files for me to analyze from."
            ),
            error="No files provided",
            stop=True,
        )

    pdf_files = [file for file in files if file.mime_type == "application/pdf"]
    text_files = [file for file in files if file.mime_type == "text/plain"]

    content_extracted = []

    if pdf_files:
        try:
            extractor_response = data_engineer_agent.run(
                f"""
                You are given guidelines in what to extract and files.
                You need to extract the information from the file to the best extent of the guidelines.

                GUIDELINES:
                {previous_step_content.information_extract_guidelines}
                """,
                files=files,
            )
            extracted_contents = extractor_response.content
            if extracted_contents.extracted_content:
                content_extracted.append(extracted_contents.extracted_content)
        except Exception as e:
            return StepOutput(
                success=False,
                content=AgentFinalResponse(error_message=f"An error has occurred: {e}"),
                error=f"An error has occurred: {e}",
                stop=True,
            )

    if text_files:
        text_content_extracted = "\n".join(
            [text_file.content.decode("utf-8") for text_file in text_files]
        )
        try:
            extractor_response = data_engineer_agent.run(
                f"""
                You are given guidelines in what to extract and the content in plain text.
                You need to extract the information from the content to the best extent of the guidelines.

                GUIDELINES:
                {previous_step_content.information_extract_guidelines}

                <content>
                {text_content_extracted}
                </content>
                """,
            )
            extracted_contents = extractor_response.content
            if extracted_contents.extracted_content:
                content_extracted.append(extracted_contents.extracted_content)
        except Exception as e:
            return StepOutput(
                success=False,
                content=AgentFinalResponse(error_message=f"An error has occurred: {e}"),
                error=f"An error has occurred: {e}",
                stop=True,
            )

    return StepOutput(
        success=True, content=DataContextOutput(content_extracted=content_extracted)
    )


gather_data_from_context_step = Step(
    name="Gather Data From Context",
    description="Gather data from the context to answer the query.",
    executor=gather_data_from_context,
    max_retries=1,
)
