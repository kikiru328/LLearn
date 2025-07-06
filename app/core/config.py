from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Setting for Apps (Dependency)"""

    environment: str = "development"  # 기본값만 넣어둠
    openai_api_key: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="allow"
    )

settings = Settings()
