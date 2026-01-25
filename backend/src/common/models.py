"""
Data models for the RAG system.

This module contains the core data models used throughout the system.
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, field_validator
from uuid import uuid4


class ContentChunk(BaseModel):
    """Represents a segment of text extracted from a Docusaurus page."""

    id: str
    content: str
    source_url: str
    title: str
    section: str = ""
    chunk_index: int = 0
    created_at: datetime
    embedding: Optional[List[float]] = None

    @field_validator('content')
    @classmethod
    def validate_content(cls, v):
        if not v or not v.strip():
            raise ValueError('content must not be empty')
        return v

    @field_validator('source_url')
    @classmethod
    def validate_source_url(cls, v):
        if not v.startswith(('http://', 'https://')):
            raise ValueError('source_url must be a valid URL')
        return v

    @field_validator('chunk_index')
    @classmethod
    def validate_chunk_index(cls, v):
        if v < 0:
            raise ValueError('chunk_index must be non-negative')
        return v

    def __init__(self, **data):
        if 'id' not in data:
            data['id'] = str(uuid4())
        if 'created_at' not in data:
            data['created_at'] = datetime.now()
        super().__init__(**data)


class EmbeddingRecord(BaseModel):
    """A vector representation of content chunk stored in Qdrant with associated metadata."""

    id: str
    vector: List[float]
    metadata: Dict[str, Any]
    created_at: datetime

    @field_validator('vector')
    @classmethod
    def validate_vector(cls, v):
        if not v or len(v) == 0:
            raise ValueError('vector must not be empty')
        return v

    @field_validator('metadata')
    @classmethod
    def validate_metadata(cls, v):
        required_fields = ['source_url', 'title']
        for field in required_fields:
            if field not in v:
                raise ValueError(f'metadata must include required field: {field}')
        return v

    def __init__(self, **data):
        if 'id' not in data:
            data['id'] = str(uuid4())
        if 'created_at' not in data:
            data['created_at'] = datetime.now()
        super().__init__(**data)


class CrawlJob(BaseModel):
    """Represents a single ingestion process that includes configuration, status, and results."""

    id: str
    urls: List[str]
    status: str
    start_time: datetime
    end_time: Optional[datetime] = None
    processed_count: int = 0
    failed_count: int = 0
    error_details: List[Dict] = []
    config: Dict[str, Any] = {}

    @field_validator('urls')
    @classmethod
    def validate_urls(cls, v):
        if not v:
            raise ValueError('urls must not be empty')
        return v

    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        valid_statuses = ['pending', 'in_progress', 'completed', 'failed']
        if v not in valid_statuses:
            raise ValueError(f'status must be one of {valid_statuses}')
        return v

    @field_validator('processed_count', 'failed_count')
    @classmethod
    def validate_counts(cls, v):
        if v < 0:
            raise ValueError('counts must be non-negative')
        return v

    def __init__(self, **data):
        if 'id' not in data:
            data['id'] = str(uuid4())
        if 'start_time' not in data:
            data['start_time'] = datetime.now()
        if 'status' not in data:
            data['status'] = 'pending'
        super().__init__(**data)