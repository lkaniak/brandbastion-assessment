from agno.vectordb.chroma import ChromaDb
from agno.knowledge.combined import CombinedKnowledgeBase
from agno.knowledge.pdf import PDFKnowledgeBase
from agno.knowledge.text import TextKnowledgeBase
from src.config import app_settings
from src.memory.embedder import embedder

vector_storage_config = {
    "path": app_settings.CHROMA_DB_PERSISTENT_PATH,
    "persistent_client": True,
    "embedder": embedder,
}

vector_storage_pdf = ChromaDb(**vector_storage_config, collection="reports")

vector_storage_text = ChromaDb(**vector_storage_config, collection="comments")

knowledge_base = CombinedKnowledgeBase(
    vector_db=ChromaDb(**vector_storage_config, collection="combined_docs"),
    sources=[
        PDFKnowledgeBase(vector_db=vector_storage_pdf, path=""),
        TextKnowledgeBase(vector_db=vector_storage_text, path=""),
    ],
)
