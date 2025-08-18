from agno.tools import tool
from typing import List, Dict, Any, Optional
from src.tools.file_processor_tool.file_processor import file_processor


@tool
def create_analysis_context(processed_files: Dict[str, Any], user_query: str = "") -> Dict[str, Any]:
    """
    Create an analysis context from processed files and user query.

    This tool takes the output from handle_file_upload and creates a structured
    context for analysis, combining file contents with the user's query.

    Args:
        processed_files: Output from handle_file_upload function
        user_query: The user's original query or question

    Returns:
        Dictionary containing:
            - status: Success/failure status
            - context_content: The complete context for analysis
            - file_summary: Summary of files included in context
            - analysis_ready: Whether the context is ready for analysis
    """
    try:
        successful_files = [f for f in processed_files.get("processed_files", []) if f["status"] == "success"]

        if not successful_files:
            return {
                "status": "no_files",
                "context_content": f"User Query: {user_query}\n\nNo files were successfully processed.",
                "file_summary": "No files processed",
                "analysis_ready": False,
            }

        # Create context content
        context_parts = []

        if user_query:
            context_parts.append(f"USER QUERY: {user_query}")
            context_parts.append("")

        context_parts.append("UPLOADED FILES CONTENT:")
        context_parts.append("=" * 50)

        total_content_length = 0
        for file_info in successful_files:
            filename = file_info["filename"]
            content = file_info["extracted_content"]
            content_length = len(content)
            total_content_length += content_length

            context_parts.append(f"\nFILE: {filename}")
            context_parts.append(f"TYPE: {file_info['content_type']}")
            context_parts.append(f"SIZE: {file_info['size']} bytes")
            context_parts.append("-" * 30)
            context_parts.append(content)
            context_parts.append("=" * 50)

        context_content = "\n".join(context_parts)

        return {
            "status": "success",
            "context_content": context_content,
            "file_summary": f"{len(successful_files)} files processed, {total_content_length} characters of content",
            "analysis_ready": True,
            "file_count": len(successful_files),
            "total_content_length": total_content_length,
        }

    except Exception as e:
        return {
            "status": "error",
            "context_content": f"Error creating analysis context: {str(e)}",
            "file_summary": "Error occurred",
            "analysis_ready": False,
        }


@tool
def process_uploaded_files(files: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Process uploaded files and extract their content for analysis.

    This tool takes a list of uploaded files and extracts their text content.
    It supports PDF files, text files, and provides metadata for image files.

    Args:
        files: List of file objects. Each file should have:
            - filename: Name of the file
            - content_type: MIME type of the file
            - content: Binary content of the file

    Returns:
        Dictionary containing:
            - processed_files: List of processed file information
            - total_files: Total number of files processed
            - successful_files: Number of successfully processed files
            - summary: Human-readable summary of the processing results
    """
    # Add debugging information
    print(f"DEBUG: process_uploaded_files called with {len(files)} files")
    for i, file_info in enumerate(files):
        print(f"DEBUG: File {i}: keys={list(file_info.keys())}, type={type(file_info)}")
        if hasattr(file_info, "name"):
            print(f"DEBUG: File {i} has name attribute: {file_info.name}")

    result = file_processor.process_files(files)
    print(f"DEBUG: process_uploaded_files result: {result}")
    return result


@tool
def add_files_to_context(processed_files: Dict[str, Any], context_description: str = "") -> Dict[str, Any]:
    """
    Add processed files to the agent's context for analysis.

    This tool takes the output from process_uploaded_files and adds the file contents
    to the agent's working context for analysis.

    Args:
        processed_files: Output from process_uploaded_files function
        context_description: Optional description of the context these files represent

    Returns:
        Dictionary containing:
            - status: Success/failure status
            - context_summary: Summary of what was added to context
            - file_count: Number of files added to context
            - content_length: Total length of content added
    """
    try:
        successful_files = [f for f in processed_files.get("processed_files", []) if f["status"] == "success"]

        if not successful_files:
            return {
                "status": "no_files",
                "context_summary": "No files were successfully processed to add to context",
                "file_count": 0,
                "content_length": 0,
            }

        context_parts = []
        if context_description:
            context_parts.append(f"Context: {context_description}")

        context_parts.append("Uploaded Files Content:")

        total_content_length = 0
        for file_info in successful_files:
            filename = file_info["filename"]
            content = file_info["extracted_content"]
            content_length = len(content)
            total_content_length += content_length

            context_parts.append(f"\n--- File: {filename} ---")
            context_parts.append(content)
            context_parts.append("--- End File ---\n")

        context_content = "\n".join(context_parts)

        return {
            "status": "success",
            "context_summary": f"Added {len(successful_files)} files to context",
            "file_count": len(successful_files),
            "content_length": total_content_length,
            "context_content": context_content,
        }

    except Exception as e:
        return {
            "status": "error",
            "context_summary": f"Error adding files to context: {str(e)}",
            "file_count": 0,
            "content_length": 0,
        }
