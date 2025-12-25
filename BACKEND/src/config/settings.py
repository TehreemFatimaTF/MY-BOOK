"""
Configuration management with secure API key handling
"""
from pydantic_settings import BaseSettings
from typing import Optional, List
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # API Keys and endpoints
    cohere_api_key: str = ""
    qdrant_api_key: str = ""
    qdrant_cluster_endpoint: str = ""
    neon_db_url: str = ""
    gemini_api_key: str = ""
    

    # Application settings
    app_name: str = "Book RAG Chatbot"
    app_version: str = "0.1.0"
    debug: bool = False

    # API settings
    api_v1_prefix: str = "/api/v1"
    allowed_origins: List[str] = ["http://localhost:3000/"]  # Should be configured based on deployment

    # Cohere settings
    cohere_model: str = "command-r-plus"  # Default model for generation
    cohere_embedding_model: str = "embed-english-v3.0"  # Default model for embeddings

    # Qdrant settings
    qdrant_collection_name: str = "book_content_chunks"

    # Database settings
    postgres_pool_size: int = 20
    postgres_pool_timeout: int = 30

    # Performance settings
    max_query_length: int = 1000  # Maximum length of user queries
    max_selected_text_length: int = 5000  # Maximum length of selected text
    response_timeout: int = 30  # Timeout for API responses in seconds

    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
        "extra": "ignore"  # This will ignore extra fields that aren't defined in the model
    }

# Create a single instance of settings
settings = Settings()

def validate_config():
    """
    Validate that required configuration values are present
    """
    errors = []

    if not settings.cohere_api_key:
        errors.append("COHERE_API_KEY is not set")

    if not settings.qdrant_api_key:
        errors.append("QDRANT_API_KEY is not set")

    if not settings.qdrant_cluster_endpoint:
        errors.append("QDRANT_CLUSTER_ENDPOINT is not set")

    if not settings.neon_db_url:
        errors.append("NEON_DB_URL is not set")

    if errors:
        raise ValueError(f"Configuration validation failed: {'; '.join(errors)}")

    print("Configuration validation passed.")
