from typing import List, Dict, Any
import pypdf
import io


class FileProcessor:
    """Tool for processing uploaded files with standard format"""

    def __init__(self):
        self.supported_types = {
            "application/pdf": self._process_pdf,
            "text/plain": self._process_text,
            "text/csv": self._process_text,
            "image/jpeg": self._process_image,
            "image/png": self._process_image,
            "image/gif": self._process_image,
        }

    def _process_pdf(self, content: bytes, filename: str) -> str:
        """Extract text content from PDF files"""
        try:
            pdf_reader = pypdf.PdfReader(io.BytesIO(content))
            text_content = []

            for page_num, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                if page_text.strip():
                    text_content.append(f"Page {page_num + 1}:\n{page_text}")

            return "\n\n".join(text_content) if text_content else "No text content found in PDF"
        except Exception as e:
            return f"Error extracting PDF content: {str(e)}"

    def _process_text(self, content: bytes, filename: str) -> str:
        """Extract text content from text files"""
        try:
            try:
                return content.decode("utf-8")
            except UnicodeDecodeError:
                return content.decode("latin-1")
        except Exception as e:
            return f"Error reading text file: {str(e)}"

    def _process_image(self, content: bytes, filename: str) -> str:
        """Process image files - return metadata since we can't extract text from images"""
        return (
            f"Image file: {filename} (size: {len(content)} bytes). Image content cannot be extracted as text."
        )

    def _generate_summary(self, processed_files: List[Dict[str, Any]]) -> str:
        """Generate a summary of processed files"""
        total = len(processed_files)
        successful = len([f for f in processed_files if f["status"] == "success"])
        errors = len([f for f in processed_files if f["status"] == "error"])
        unsupported = len([f for f in processed_files if f["status"] == "unsupported_type"])

        summary = f"Processed {total} files:\n"
        summary += f"- Successfully processed: {successful}\n"
        summary += f"- Errors: {errors}\n"
        summary += f"- Unsupported types: {unsupported}\n"

        if successful > 0:
            summary += "\nSuccessfully processed files:\n"
            for file in processed_files:
                if file["status"] == "success":
                    summary += f"- {file['filename']} ({file['content_type']})\n"

        return summary

    def _process_files_common(
        self, files: List[Dict[str, Any]], handle_unsupported_as_error: bool = False
    ) -> Dict[str, Any]:
        """
        Common file processing logic shared between implementations

        Args:
            files: List of file objects
            handle_unsupported_as_error: If True, raise ValueError for unsupported types instead of marking as unsupported

        Returns:
            Dictionary containing processed file contents and metadata
        """
        processed_files = []

        for file_info in files:
            try:
                filename, content_type, content = self._extract_file_info(file_info)

                if content_type in self.supported_types:
                    processor = self.supported_types[content_type]
                    extracted_content = processor(content, filename)

                    processed_files.append(
                        {
                            "filename": filename,
                            "content_type": content_type,
                            "extracted_content": extracted_content,
                            "size": len(content),
                            "status": "success",
                        }
                    )
                else:
                    if handle_unsupported_as_error:
                        raise ValueError(f"Unsupported file type: {content_type}")
                    else:
                        processed_files.append(
                            {
                                "filename": filename,
                                "content_type": content_type,
                                "extracted_content": f"Unsupported file type: {content_type}",
                                "size": len(content),
                                "status": "unsupported_type",
                            }
                        )

            except Exception as e:
                # For error handling, we need to get the original file info
                filename = file_info.get("filename", file_info.get("name", "unknown"))
                content_type = file_info.get("content_type", file_info.get("type", "unknown"))
                content = file_info.get("content", b"")

                processed_files.append(
                    {
                        "filename": filename,
                        "content_type": content_type,
                        "extracted_content": f"Error processing file: {str(e)}",
                        "size": len(content),
                        "status": "error",
                    }
                )

        return {
            "processed_files": processed_files,
            "total_files": len(files),
            "successful_files": len([f for f in processed_files if f["status"] == "success"]),
            "summary": self._generate_summary(processed_files),
        }

    def _extract_file_info(self, file_info: Dict[str, Any]) -> tuple[str, str, bytes]:
        """Extract file info from agno playground format"""
        filename = file_info.get("name", file_info.get("filename", "unknown"))
        content_type = file_info.get("type", file_info.get("content_type", "application/octet-stream"))

        content = None

        # Handle different file formats from Agno playground
        if "content" in file_info:
            content = file_info["content"]
        elif "data" in file_info:
            content = file_info["data"]
        elif "file" in file_info:
            file_obj = file_info["file"]
            if hasattr(file_obj, "read"):
                content = file_obj.read()
            elif hasattr(file_obj, "file"):
                content = file_obj.file.read()
        elif "bytes" in file_info:
            content = file_info["bytes"]
        elif "binary" in file_info:
            content = file_info["binary"]

        # Handle FormData format from frontend
        if hasattr(file_info, "read") and hasattr(file_info, "name"):
            # This is a file-like object from FormData
            content = file_info.read()
            filename = file_info.name
            content_type = getattr(file_info, "type", "application/octet-stream")

        if content is None:
            raise ValueError(
                f"Could not read file content for {filename}. Available keys: {list(file_info.keys())}"
            )

        if isinstance(content, str):
            content = content.encode("utf-8")

        return filename, content_type, content

    def process_files(self, files: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Process a list of uploaded files and extract their content

        Args:
            files: List of file objects with 'filename', 'content_type', and 'content' keys

        Returns:
            Dictionary containing processed file contents and metadata
        """
        return self._process_files_common(files)


file_processor = FileProcessor()
