"""
Chunking service for the RAG system.

This module orchestrates the chunking operations.
"""

import logging
from typing import List

from config.settings import ProcessingConfig
from src.common.models import ContentChunk
from .text_chunker import TextChunker


class ChunkerService:
    """Coordinates chunking operations."""

    def __init__(self, config: ProcessingConfig):
        """
        Initialize the chunker service.

        Args:
            config: Processing configuration
        """
        self.config = config
        self.text_chunker = TextChunker(config)
        self.logger = logging.getLogger(__name__)

    def process_content_chunks(self, content_chunks: List[ContentChunk]) -> List[ContentChunk]:
        """
        Process a list of content chunks by re-chunking them to appropriate size.

        Args:
            content_chunks: List of ContentChunk objects to process

        Returns:
            List of re-chunked ContentChunk objects
        """
        processed_chunks = []

        for chunk in content_chunks:
            # Validate the chunk quality before processing
            is_valid, issues = self.text_chunker.validate_chunk_quality(chunk)
            if not is_valid:
                self.logger.warning(f"Invalid chunk from {chunk.source_url}: {', '.join(issues)}")
                continue

            # If the chunk is already appropriately sized, keep it as is
            if len(chunk.content) <= self.config.chunk_size:
                processed_chunks.append(chunk)
            else:
                # Otherwise, split it into smaller chunks
                sub_chunks = self.text_chunker.chunk_text(
                    chunk.content,
                    chunk.source_url,
                    chunk.title,
                    chunk.section
                )
                processed_chunks.extend(sub_chunks)

        self.logger.info(f"Processed {len(content_chunks)} input chunks into {len(processed_chunks)} output chunks")
        return processed_chunks

    def chunk_text_content(
        self,
        text: str,
        source_url: str,
        title: str,
        section: str = ""
    ) -> List[ContentChunk]:
        """
        Chunk a text string directly.

        Args:
            text: Text to chunk
            source_url: URL where text was found
            title: Title of the page
            section: Section/heading context (optional)

        Returns:
            List of ContentChunk objects
        """
        return self.text_chunker.chunk_text(text, source_url, title, section)

    def validate_chunks(self, chunks: List[ContentChunk]) -> List[ContentChunk]:
        """
        Validate a list of chunks and return only valid ones.

        Args:
            chunks: List of ContentChunk objects to validate

        Returns:
            List of valid ContentChunk objects
        """
        valid_chunks = []
        for chunk in chunks:
            is_valid, issues = self.text_chunker.validate_chunk_quality(chunk)
            if is_valid:
                valid_chunks.append(chunk)
            else:
                self.logger.warning(f"Invalid chunk from {chunk.source_url}: {', '.join(issues)}")

        if len(valid_chunks) != len(chunks):
            self.logger.info(f"Validated {len(chunks)} chunks, {len(valid_chunks)} passed validation")

        return valid_chunks