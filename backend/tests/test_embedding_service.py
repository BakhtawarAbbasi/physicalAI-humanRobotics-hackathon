"""
Test suite for the embedding service functionality.
"""
import os
import pytest
from unittest.mock import Mock, patch, MagicMock

from config.settings import ProcessingConfig
from src.common.models import ContentChunk, EmbeddingRecord
from src.embedding.embedding_service import EmbeddingService
from src.embedding.cohere_embedder import CohereEmbedder
from src.storage.qdrant_storage import QdrantStorage


class TestEmbeddingService:
    """Test cases for the EmbeddingService class."""

    @pytest.fixture
    def config(self):
        """Create a mock configuration for testing."""
        config = Mock(spec=ProcessingConfig)
        config.cohere_api_key = "test-key"
        config.qdrant_url = "https://test.qdrant.com"
        config.qdrant_api_key = "test-qdrant-key"
        config.chunk_size = 1000
        config.chunk_overlap = 200
        return config

    @pytest.fixture
    def content_chunks(self):
        """Create sample content chunks for testing."""
        return [
            ContentChunk(
                content="This is a test content chunk for embedding.",
                source_url="https://example.com/test",
                title="Test Page"
            ),
            ContentChunk(
                content="Another test content chunk with different content.",
                source_url="https://example.com/test2",
                title="Test Page 2"
            )
        ]

    @pytest.fixture
    def embedding_service(self, config):
        """Create an embedding service instance for testing."""
        with patch('src.embedding.cohere_embedder.cohere.Client'), \
             patch('src.storage.qdrant_storage.QdrantClient'):
            service = EmbeddingService(config)
            # Mock the embedder and storage to avoid external API calls
            service.embedder = Mock(spec=CohereEmbedder)
            service.storage = Mock(spec=QdrantStorage)
            return service

    def test_embedding_service_initialization(self, config):
        """Test that the embedding service initializes correctly."""
        with patch('src.embedding.cohere_embedder.cohere.Client'), \
             patch('src.storage.qdrant_storage.QdrantClient'):
            service = EmbeddingService(config)
            assert service.config == config
            assert service.embedder is not None
            assert service.storage is not None

    def test_generate_and_store_embeddings_success(self, embedding_service, content_chunks):
        """Test successful embedding generation and storage."""
        # Mock the embedder to return embedding records
        mock_embedding_records = [
            EmbeddingRecord(
                vector=[0.1, 0.2, 0.3] * 341 + [0.4],  # 1024 dimensions
                metadata={"source_url": "https://example.com/test", "title": "Test Page"}
            )
        ]
        embedding_service.embedder.embed_content_chunks.return_value = mock_embedding_records
        embedding_service.storage.validate_embedding_dimensions.return_value = True
        embedding_service.storage.store_embeddings.return_value = True

        result = embedding_service.generate_and_store_embeddings(content_chunks)

        assert result is True
        embedding_service.embedder.embed_content_chunks.assert_called_once_with(content_chunks)
        embedding_service.storage.store_embeddings.assert_called_once_with(mock_embedding_records)

    def test_generate_and_store_embeddings_empty_chunks(self, embedding_service):
        """Test handling of empty content chunks list."""
        result = embedding_service.generate_and_store_embeddings([])
        assert result is True
        embedding_service.embedder.embed_content_chunks.assert_not_called()
        embedding_service.storage.store_embeddings.assert_not_called()

    def test_generate_and_store_embeddings_validation_failure(self, embedding_service, content_chunks):
        """Test handling when embedding validation fails."""
        mock_embedding_records = [
            EmbeddingRecord(
                vector=[0.1, 0.2, 0.3] * 341 + [0.4],  # 1024 dimensions
                metadata={"source_url": "https://example.com/test", "title": "Test Page"}
            )
        ]
        embedding_service.embedder.embed_content_chunks.return_value = mock_embedding_records
        embedding_service.storage.validate_embedding_dimensions.return_value = False

        with pytest.raises(Exception):
            embedding_service.generate_and_store_embeddings(content_chunks)

    def test_embed_and_store_single_chunk_success(self, embedding_service):
        """Test successful embedding and storage of a single chunk."""
        content_chunk = ContentChunk(
            content="Test content for single chunk embedding.",
            source_url="https://example.com/test",
            title="Test Page"
        )

        mock_embedding_record = EmbeddingRecord(
            vector=[0.1, 0.2, 0.3] * 341 + [0.4],  # 1024 dimensions
            metadata={"source_url": "https://example.com/test", "title": "Test Page"}
        )

        embedding_service.embedder.embed_single_chunk.return_value = mock_embedding_record
        embedding_service.storage.validate_embedding_dimensions.return_value = True
        embedding_service.storage.store_single_embedding.return_value = True

        result = embedding_service.embed_and_store_single_chunk(content_chunk)

        assert result is True
        embedding_service.embedder.embed_single_chunk.assert_called_once_with(content_chunk)
        embedding_service.storage.store_single_embedding.assert_called_once_with(mock_embedding_record)

    def test_validate_embedding_consistency_valid(self, embedding_service):
        """Test validation of consistent embeddings."""
        valid_records = [
            EmbeddingRecord(
                vector=[0.1] * 1024,  # 1024 dimensions
                metadata={"source_url": "https://example.com/test", "title": "Test Page"}
            )
        ]

        result = embedding_service.validate_embedding_consistency(valid_records)
        assert result is True

    def test_validate_embedding_consistency_invalid_size(self, embedding_service):
        """Test validation fails for embeddings with wrong size."""
        invalid_records = [
            EmbeddingRecord(
                vector=[0.1] * 512,  # Wrong size - only 512 dimensions
                metadata={"source_url": "https://example.com/test", "title": "Test Page"}
            )
        ]

        result = embedding_service.validate_embedding_consistency(invalid_records)
        assert result is False

    def test_validate_embedding_consistency_with_nan(self, embedding_service):
        """Test validation fails for embeddings with NaN values."""
        import math
        invalid_records = [
            EmbeddingRecord(
                vector=[0.1] * 511 + [float('nan')] + [0.2] * 512,  # Contains NaN
                metadata={"source_url": "https://example.com/test", "title": "Test Page"}
            )
        ]

        result = embedding_service.validate_embedding_consistency(invalid_records)
        assert result is False

    def test_validate_and_process_chunks(self, embedding_service, content_chunks):
        """Test validation and processing of content chunks."""
        # Add an invalid chunk to the list
        invalid_chunk = ContentChunk(
            content="",
            source_url="",
            title=""
        )
        all_chunks = content_chunks + [invalid_chunk]

        result = embedding_service.validate_and_process_chunks(all_chunks)

        # Should return only the valid chunks
        assert len(result) == len(content_chunks)
        assert all(chunk in result for chunk in content_chunks)