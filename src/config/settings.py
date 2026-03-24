"""Application configuration settings"""
from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    model_config = ConfigDict(env_file=".env", case_sensitive=False)
    
    # OpenAI
    openai_api_key: str
    
    # MongoDB
    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_db_name: str = "healthy_food_ai"
    
    # Application
    debug: bool = False
    log_level: str = "INFO"


settings = Settings()
