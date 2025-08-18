from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_ignore_empty=True, extra="ignore")

    HUGGINGFACE_API_KEY: str
    OPENAI_API_KEY: str

    CHROMA_DB_PERSISTENT_PATH: str = "~/.chroma"


app_settings = Settings()
