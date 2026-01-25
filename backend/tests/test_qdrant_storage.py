"""
Test suite for the Qdrant storage functionality.
"""
import os
import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

from config.settings import ProcessingConfig
from src.common.models import EmbeddingRecord
from src.storage.qdrant_storage import QdrantStorage


class TestQdrantStorage:
    """Test cases for the QdrantStorage class."""

    @pytest.fixture
    def config(self):
        """Create a mock configuration for testing."""
        config = Mock(spec=ProcessingConfig)
        config.qdrant_url = "https://test.qdrant.com"
        config.qdrant_api_key = "test-qdrant-key"
        return config

    @pytest.fixture
    def embedding_records(self):
        """Create sample embedding records for testing."""
        return [
            EmbeddingRecord(
                vector=[0.1, 0.2, 0.3] * 341 + [0.4],  # 1024 dimensions
                metadata={"source_url": "https://example.com/test", "title": "Test Page", "section": "Introduction"},
                created_at=datetime.now()
            ),
            EmbeddingRecord(
                vector=[0.5, 0.6, 0.7] * 341 + [0.8],  # 1024 dimensions
                metadata={"source_url": "https://example.com/test2", "title": "Test Page 2", "section": "Conclusion"},
                created_at=datetime.now()
            )
        ]

    @pytest.fixture
    def qdrant_storage(self, config):
        """Create a Qdrant storage instance for testing."""
        with patch('src.storage.qdrant_storage.QdrantClient') as mock_client:
            storage = QdrantStorage(config)
            # Replace the actual client with a mock
            storage.client = mock_client.return_value
            return storage

    def test_qdrant_storage_initialization(self, config):
        """Test that the Qdrant storage initializes correctly."""
        with patch('src.storage.qdrant_storage.QdrantClient') as mock_client:
            storage = QdrantStorage(config)

            # Verify client was initialized with correct parameters
            mock_client.assert_called_once_with(
                url=config.qdrant_url,
                api_key=config.qdrant_api_key,
                https=True
            )
            assert storage.collection_name == "content_embeddings"

    def test_initialize_collection_new(self, config):
        """Test initialization of a new collection."""
        with patch('src.storage.qdrant_storage.QdrantClient') as mock_client:
            mock_client_instance = Mock()
            mock_client.return_value = mock_client_instance

            # Mock the get_collections method to return an empty list
            mock_collections = Mock()
            mock_collections.collections = []
            mock_client_instance.get_collections.return_value = mock_collections

            storage = QdrantStorage(config)

            # Verify that create_collection was called
            mock_client_instance.create_collection.assert_called_once()
            args, kwargs = mock_client_instance.create_collection.call_args
            assert kwargs['collection_name'] == "content_embeddings"
            assert kwargs['vectors_config'].size == 1024
            assert str(kwargs['vectors_config'].distance) == "cosine"

    def test_initialize_collection_exists(self, config):
        """Test initialization when collection already exists."""
        with patch('src.storage.qdrant_storage.QdrantClient') as mock_client:
            mock_client_instance = Mock()
            mock_client.return_value = mock_client_instance

            # Mock the get_collections method to return a list with our collection
            mock_collection = Mock()
            mock_collection.name = "content_embeddings"
            mock_collections = Mock()
            mock_collections.collections = [mock_collection]
            mock_client_instance.get_collections.return_value = mock_collections

            storage = QdrantStorage(config)

            # Verify that create_collection was not called
            mock_client_instance.create_collection.assert_not_called()

    def test_store_embeddings_success(self, qdrant_storage, embedding_records):
        """Test successful storage of embeddings."""
        qdrant_storage.client.upsert.return_value = True

        result = qdrant_storage.store_embeddings(embedding_records)

        assert result is True
        qdrant_storage.client.upsert.assert_called_once()
        args, kwargs = qdrant_storage.client.upsert.call_args
        assert kwargs['collection_name'] == "content_embeddings"
        assert len(kwargs['points']) == len(embedding_records)

    def test_store_embeddings_empty_list(self, qdrant_storage):
        """Test storage of empty embeddings list."""
        result = qdrant_storage.store_embeddings([])

        assert result is True
        qdrant_storage.client.upsert.assert_not_called()

    def test_store_single_embedding(self, qdrant_storage, embedding_records):
        """Test storage of a single embedding."""
        qdrant_storage.client.upsert.return_value = True

        result = qdrant_storage.store_single_embedding(embedding_records[0])

        assert result is True
        qdrant_storage.client.upsert.assert_called_once()
        args, kwargs = qdrant_storage.client.upsert.call_args
        assert len(kwargs['points']) == 1

    def test_search_embeddings(self, qdrant_storage):
        """Test searching for embeddings."""
        # Mock search results
        mock_result = Mock()
        mock_result.id = "test-id"
        mock_result.score = 0.95
        mock_result.payload = {"source_url": "https://example.com", "title": "Test"}
        mock_result.vector = [0.1, 0.2, 0.3]

        qdrant_storage.client.search.return_value = [mock_result]

        query_vector = [0.1, 0.2, 0.3] * 341 + [0.4]  # 1024 dimensions
        results = qdrant_storage.search_embeddings(query_vector, limit=5)

        assert len(results) == 1
        assert results[0]["id"] == "test-id"
        assert results[0]["score"] == 0.95
        assert results[0]["payload"]["source_url"] == "https://example.com"

    def test_validate_embedding_dimensions_correct(self, qdrant_storage, embedding_records):
        """Test validation of embeddings with correct dimensions."""
        result = qdrant_storage.validate_embedding_dimensions(embedding_records)
        assert result is True

    def test_validate_embedding_dimensions_incorrect(self, qdrant_storage):
        """Test validation of embeddings with incorrect dimensions."""
        invalid_record = EmbeddingRecord(
            vector=[0.1, 0.2, 0.3],  # Only 3 dimensions instead of 1024
            metadata={"source_url": "https://example.com/test", "title": "Test Page"},
            created_at=datetime.now()
        )

        result = qdrant_storage.validate_embedding_dimensions([invalid_record])
        assert result is False

    def test_validate_embedding_dimensions_empty(self, qdrant_storage):
        """Test validation of empty embeddings list."""
        result = qdrant_storage.validate_embedding_dimensions([])
        assert result is True

    def test_get_collection_info(self, qdrant_storage):
        """Test getting collection information."""
        # Mock collection info
        mock_config = Mock()
        mock_params = Mock()
        mock_params.vectors.size = 1024
        mock_params.vectors.distance = "cosine"
        mock_config.params = mock_params

        mock_collection_info = Mock()
        mock_collection_info.config = mock_config
        mock_collection_info.points_count = 100

        qdrant_storage.client.get_collection.return_value = mock_collection_info

        info = qdrant_storage.get_collection_info()

        assert info["vector_size"] == 1024
        assert info["distance"] == "cosine"
        assert info["point_count"] == 100

    def test_close_connection(self, qdrant_storage):
        """Test closing the Qdrant client connection."""
        qdrant_storage.close()
        qdrant_storage.client.close.assert_called_once()