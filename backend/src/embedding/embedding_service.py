"""
Embedding service for the RAG system.

This module orchestrates the embedding and storage operations.
"""

import logging
from typing import List

from config.settings import ProcessingConfig
from src.common.exceptions import EmbeddingException, StorageException
from src.common.models import ContentChunk, EmbeddingRecord
from .cohere_embedder import CohereEmbedder
from ..storage.qdrant_storage import QdrantStorage


class EmbeddingService:
    """Coordinates embedding generation and storage operations."""

    def __init__(self, config: ProcessingConfig):
        """
        Initialize the embedding service.

        Args:
            config: Processing configuration
        """
        self.config = config
        self.embedder = CohereEmbedder(config)
        self.storage = QdrantStorage(config)
        self.logger = logging.getLogger(__name__)

    def generate_and_store_embeddings(self, content_chunks: List[ContentChunk]) -> bool:
        """
        Generate embeddings for content chunks and store them in Qdrant.

        Args:
            content_chunks: List of ContentChunk objects to process

        Returns:
            True if successful, False otherwise
        """
        if not content_chunks:
            self.logger.info("No content chunks to process")
            return True

        try:
            self.logger.info(f"Starting embedding generation for {len(content_chunks)} content chunks")

            # Validate content chunks before processing
            valid_chunks = self.validate_and_process_chunks(content_chunks)
            if not valid_chunks:
                self.logger.warning("No valid content chunks to process")
                return True

            # Generate embeddings for the content chunks
            embedding_records = self.embedder.embed_content_chunks(valid_chunks)

            self.logger.info(f"Generated {len(embedding_records)} embedding records")

            # Validate embedding dimensions before storing
            if not self.validate_embedding_consistency(embedding_records):
                raise EmbeddingException("Embedding dimension validation failed")

            # Store embeddings in Qdrant
            success = self.storage.store_embeddings(embedding_records)

            if success:
                self.logger.info(f"Successfully stored {len(embedding_records)} embeddings in Qdrant")
                return True
            else:
                self.logger.error("Failed to store embeddings in Qdrant")
                return False

        except EmbeddingException as e:
            self.logger.error(f"Error during embedding generation: {str(e)}")
            raise
        except StorageException as e:
            self.logger.error(f"Error during storage: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error during embedding and storage: {str(e)}")
            raise EmbeddingException(f"Failed to generate and store embeddings: {str(e)}")

    def embed_and_store_single_chunk(self, content_chunk: ContentChunk) -> bool:
        """
        Generate embedding for a single content chunk and store it in Qdrant.

        Args:
            content_chunk: ContentChunk object to process

        Returns:
            True if successful, False otherwise
        """
        try:
            embedding_record = self.embedder.embed_single_chunk(content_chunk)

            # Validate embedding dimensions
            if not self.storage.validate_embedding_dimensions([embedding_record]):
                raise EmbeddingException("Embedding dimension validation failed")

            return self.storage.store_single_embedding(embedding_record)
        except Exception as e:
            self.logger.error(f"Error embedding and storing single chunk: {str(e)}")
            raise

    def validate_embedding_consistency(self, embedding_records: List[EmbeddingRecord]) -> bool:
        """
        Validate embedding dimensions and consistency across all records.

        Args:
            embedding_records: List of EmbeddingRecord objects to validate

        Returns:
            True if all embeddings are consistent, False otherwise
        """
        if not embedding_records:
            return True

        # For Cohere embed-english-v3.0, the expected size is 1024
        expected_size = 1024

        for i, record in enumerate(embedding_records):
            # Check vector dimensions
            if len(record.vector) != expected_size:
                self.logger.error(f"Embedding record {i} has incorrect size: {len(record.vector)}, expected: {expected_size}")
                return False

            # Check for NaN or infinite values in the vector
            for j, value in enumerate(record.vector):
                if not (isinstance(value, (int, float)) and value == value):  # Check for NaN
                    self.logger.error(f"Embedding record {i}, dimension {j} contains invalid value: {value}")
                    return False

        self.logger.info(f"Validated {len(embedding_records)} embedding records for consistency")
        return True

    def validate_and_process_chunks(self, content_chunks: List[ContentChunk]) -> List[ContentChunk]:
        """
        Validate content chunks before embedding and return only valid ones.

        Args:
            content_chunks: List of ContentChunk objects to validate

        Returns:
            List of valid ContentChunk objects
        """
        valid_chunks = []
        for chunk in content_chunks:
            # Basic validation
            if not chunk.content or not chunk.content.strip():
                self.logger.warning(f"Skipping empty chunk from {chunk.source_url}")
                continue

            if len(chunk.content) < 10:  # Minimum reasonable content length
                self.logger.warning(f"Skipping too short chunk from {chunk.source_url}")
                continue

            if not chunk.source_url:
                self.logger.warning(f"Skipping chunk with missing source URL")
                continue

            if not chunk.title:
                self.logger.warning(f"Skipping chunk with missing title")
                continue

            valid_chunks.append(chunk)

        self.logger.info(f"Validated {len(content_chunks)} chunks, {len(valid_chunks)} passed validation")
        return valid_chunks

    def get_storage_info(self) -> dict:
        """
        Get information about the storage collection.

        Returns:
            Dictionary with collection information
        """
        return self.storage.get_collection_info()

    def close(self):
        """Close the storage connection."""
        self.storage.close()