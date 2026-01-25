"""
Text chunking module for the RAG system.

This module handles splitting text content into appropriately sized chunks.
"""

import logging
from typing import List, Tuple

from config.settings import ProcessingConfig
from src.common.exceptions import ChunkerException
from src.common.models import ContentChunk


class TextChunker:
    """Handles text chunking with overlap and metadata preservation."""

    def __init__(self, config: ProcessingConfig):
        """
        Initialize the text chunker with configuration.

        Args:
            config: Processing configuration with chunking parameters
        """
        self.config = config
        self.logger = logging.getLogger(__name__)

    def chunk_text(
        self,
        text: str,
        source_url: str,
        title: str,
        section: str = ""
    ) -> List[ContentChunk]:
        """
        Split text into chunks with overlap and preserve metadata.

        Args:
            text: Text to chunk
            source_url: URL where text was found
            title: Title of the page
            section: Section/heading context (optional)

        Returns:
            List of ContentChunk objects
        """
        if not text or not text.strip():
            raise ChunkerException("Text cannot be empty")

        if len(text) <= self.config.chunk_size:
            # If text is smaller than chunk size, return as single chunk
            return [ContentChunk(
                content=text,
                source_url=source_url,
                title=title,
                section=section,
                chunk_index=0
            )]

        chunks = []
        start_idx = 0
        chunk_index = 0

        while start_idx < len(text):
            # Calculate end index
            end_idx = start_idx + self.config.chunk_size

            # If this is the last chunk, make sure we include all remaining text
            if end_idx >= len(text):
                end_idx = len(text)
            else:
                # Try to break at sentence boundary if possible
                end_idx = self._find_sentence_boundary(text, start_idx, end_idx)

            # Extract the chunk
            chunk_text = text[start_idx:end_idx]

            # Create ContentChunk
            chunk = ContentChunk(
                content=chunk_text,
                source_url=source_url,
                title=title,
                section=section,
                chunk_index=chunk_index
            )

            chunks.append(chunk)
            chunk_index += 1

            # Calculate next start index with overlap
            next_start = end_idx - self.config.chunk_overlap

            # Ensure we don't go backwards
            if next_start <= start_idx:
                # If overlap would cause us to repeat, move by chunk size
                start_idx += self.config.chunk_size
            else:
                start_idx = next_start

            # Prevent infinite loop
            if start_idx >= len(text):
                break

        self.logger.info(f"Split text into {len(chunks)} chunks")
        return chunks

    def _find_sentence_boundary(self, text: str, start: int, end: int) -> int:
        """
        Find the best sentence boundary near the end index.

        Args:
            text: Text to search in
            start: Start index
            end: Suggested end index

        Returns:
            Index to break the text at
        """
        # Look for sentence endings near the end
        sentence_endings = ['.', '!', '?', '\n']

        # Search backwards from the end to find a sentence boundary
        for i in range(end, max(start, end - 100), -1):
            if i < len(text) and text[i] in sentence_endings:
                # Check if it's followed by whitespace or end of text
                if i + 1 >= len(text) or text[i + 1].isspace():
                    return i + 1

        # If no sentence boundary found, try to break at word boundary
        for i in range(end, max(start, end - 100), -1):
            if i < len(text) and text[i].isspace():
                return i

        # If no good break point found, just return the original end
        return end

    def chunk_content_list(self, content_list: List[ContentChunk]) -> List[ContentChunk]:
        """
        Chunk a list of ContentChunks (for when we need to re-chunk already processed content).

        Args:
            content_list: List of ContentChunks to potentially re-chunk

        Returns:
            List of ContentChunk objects, possibly re-chunked
        """
        all_chunks = []
        for content_chunk in content_list:
            chunks = self.chunk_text(
                content_chunk.content,
                content_chunk.source_url,
                content_chunk.title,
                content_chunk.section
            )
            all_chunks.extend(chunks)

        return all_chunks

    def validate_chunk_quality(self, chunk: ContentChunk) -> Tuple[bool, List[str]]:
        """
        Validate the quality of a chunk.

        Args:
            chunk: ContentChunk to validate

        Returns:
            Tuple of (is_valid, list_of_issues)
        """
        issues = []

        if not chunk.content or not chunk.content.strip():
            issues.append("Chunk content is empty")

        if len(chunk.content) < 10:  # Minimum reasonable content length
            issues.append("Chunk content is too short")

        if not chunk.source_url:
            issues.append("Missing source URL")

        if not chunk.title:
            issues.append("Missing title")

        return len(issues) == 0, issues