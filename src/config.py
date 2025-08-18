from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_ignore_empty=True, extra="ignore")

    HUGGINGFACE_API_KEY: str
    OPENAI_API_KEY: str

    CHROMA_DB_PERSISTENT_PATH: str = "~/.chroma"

    SESSION_ID: str = "user_session_123"
    USER_ID: str = "user_123"


app_settings = Settings()
