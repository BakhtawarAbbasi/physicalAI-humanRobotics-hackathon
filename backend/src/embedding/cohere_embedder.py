"""
Cohere embedding module for the RAG system.

This module handles generating embeddings using the Cohere API.
"""

import asyncio
import logging
from typing import List, Optional

import cohere

from config.settings import ProcessingConfig
from src.common.exceptions import EmbeddingException
from src.common.models import ContentChunk, EmbeddingRecord


class CohereEmbedder:
    """Handles generating embeddings using Cohere API."""

    def __init__(self, config: ProcessingConfig):
        """
        Initialize the Cohere embedder with configuration.

        Args:
            config: Processing configuration with Cohere API key
        """
        self.config = config
        self.client = cohere.Client(config.cohere_api_key)
        self.logger = logging.getLogger(__name__)

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts using Cohere.

        Args:
            texts: List of text strings to embed

        Returns:
            List of embedding vectors (lists of floats)
        """
        if not texts:
            return []

        try:
            # Cohere has limits on batch size, so we may need to process in chunks
            batch_size = 96  # Conservative batch size (Cohere's max is 96)
            all_embeddings = []

            for i in range(0, len(texts), batch_size):
                batch = texts[i:i + batch_size]
                self.logger.info(f"Generating embeddings for batch {i//batch_size + 1}, size: {len(batch)}")

                response = self.client.embed(
                    texts=batch,
                    model="embed-english-v3.0",  # Using a reliable Cohere embedding model
                    input_type="search_document"  # Appropriate for document search
                )

                if hasattr(response, 'embeddings') and response.embeddings:
                    all_embeddings.extend(response.embeddings)
                elif hasattr(response, 'texts') and response.texts:  # For newer API versions
                    all_embeddings.extend(response.texts)
                else:
                    raise EmbeddingException("No embeddings returned from Cohere API")

            self.logger.info(f"Generated embeddings for {len(texts)} texts")
            return all_embeddings

        except Exception as e:
            self.logger.error(f"Error generating embeddings: {str(e)}")
            raise EmbeddingException(f"Failed to generate embeddings: {str(e)}")

    def embed_content_chunks(self, content_chunks: List[ContentChunk]) -> List[EmbeddingRecord]:
        """
        Generate embeddings for a list of ContentChunk objects.

        Args:
            content_chunks: List of ContentChunk objects to embed

        Returns:
            List of EmbeddingRecord objects
        """
        if not content_chunks:
            return []

        # Extract text content from ContentChunks
        texts = [chunk.content for chunk in content_chunks]

        # Generate embeddings
        embeddings = self.generate_embeddings(texts)

        if len(embeddings) != len(content_chunks):
            raise EmbeddingException(f"Mismatch: got {len(embeddings)} embeddings for {len(content_chunks)} chunks")

        # Create EmbeddingRecord objects with metadata
        embedding_records = []
        for i, chunk in enumerate(content_chunks):
            embedding_record = EmbeddingRecord(
                vector=embeddings[i],
                metadata={
                    "source_url": chunk.source_url,
                    "title": chunk.title,
                    "section": chunk.section,
                    "chunk_index": chunk.chunk_index,
                    "id": chunk.id,
                    "content": chunk.content  # Include the actual content
                }
            )
            embedding_records.append(embedding_record)

        self.logger.info(f"Created {len(embedding_records)} embedding records")
        return embedding_records

    def embed_single_chunk(self, content_chunk: ContentChunk) -> EmbeddingRecord:
        """
        Generate embedding for a single ContentChunk.

        Args:
            content_chunk: ContentChunk object to embed

        Returns:
            EmbeddingRecord object
        """
        embeddings = self.embed_content_chunks([content_chunk])
        if embeddings:
            return embeddings[0]
        else:
            raise EmbeddingException("Failed to generate embedding for single chunk")