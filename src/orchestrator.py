from agno.workflow.v2.workflow import Workflow
from src.memory.conversation_buffer import memory_db
from src.workflow import (
    check_query_subject_step,
    gather_data_from_context_step,
    generate_report_step,
)

social_media_analysis_workflow = Workflow(
    name="Social Media Analysis Workflow",
    description="A workflow to analyze social media data and provide insights.",
    storage=memory_db,
    steps=[
        check_query_subject_step,
        gather_data_from_context_step,
        generate_report_step,
    ],
)
