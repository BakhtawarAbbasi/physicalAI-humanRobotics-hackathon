"""
Configuration management for the RAG system.

This module handles all configuration for the ingestion pipeline
using Pydantic for validation and type safety.
"""

from pathlib import Path
from pydantic_settings import BaseSettings
from typing import List
from pydantic import field_validator

# Load environment variables from parent directory's .env file
env_path = Path(__file__).parent.parent.parent / ".env"
if env_path.exists():
    from dotenv import load_dotenv
    load_dotenv(env_path)


class ProcessingConfig(BaseSettings):
    """Configuration parameters for the ingestion pipeline."""

    # API Keys and URLs
    cohere_api_key: str
    openai_api_key: str
    openrouter_api_key: str
    qdrant_url: str
    qdrant_api_key: str

    # Chunking configuration
    chunk_size: int = 1000
    chunk_overlap: int = 200

    # Crawling configuration
    max_concurrent_requests: int = 5
    request_delay: float = 1.0
    timeout: int = 30

    # Additional fields that might be in the .env
    deploy_vercel_url: str = ""

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

    @field_validator('chunk_size')
    @classmethod
    def validate_chunk_size(cls, v):
        if v <= 0:
            raise ValueError('chunk_size must be positive')
        return v

    @field_validator('chunk_overlap')
    @classmethod
    def validate_chunk_overlap(cls, v):
        if v < 0:
            raise ValueError('chunk_overlap must be non-negative')
        return v

    @field_validator('max_concurrent_requests')
    @classmethod
    def validate_max_concurrent_requests(cls, v):
        if v <= 0:
            raise ValueError('max_concurrent_requests must be positive')
        return v

    @field_validator('request_delay')
    @classmethod
    def validate_request_delay(cls, v):
        if v < 0:
            raise ValueError('request_delay must be non-negative')
        return v

    @field_validator('timeout')
    @classmethod
    def validate_timeout(cls, v):
        if v <= 0:
            raise ValueError('timeout must be positive')
        return v

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Additional validation that requires multiple fields
        if self.chunk_overlap >= self.chunk_size:
            raise ValueError('chunk_overlap must be less than chunk_size')