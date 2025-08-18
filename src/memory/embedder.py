from agno.embedder.huggingface import HuggingfaceCustomEmbedder
from src.config import app_settings

embedder = HuggingfaceCustomEmbedder(
    id="sentence-transformers/all-MiniLM-L6-v2",
    api_key=app_settings.HUGGINGFACE_API_KEY,
)
