from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # Environment
    environment: str = Field(default="development", alias="ENVIRONMENT")

    # Mongo
    mongodb_url: str = Field(
        default="mongodb://localhost:27017",
        alias="MONGODB_URL"
    )
    mongodb_db_name: str = Field(default="child_voice", alias="MONGODB_DB_NAME")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        populate_by_name = True


# ✅ MUST exist with this exact name
settings = Settings()
