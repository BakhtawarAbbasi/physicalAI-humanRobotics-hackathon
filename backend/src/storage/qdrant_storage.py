"""
Qdrant storage module for the RAG system.

This module handles storing embeddings in Qdrant Cloud.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional

from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import PointStruct

from config.settings import ProcessingConfig
from src.common.exceptions import StorageException
from src.common.models import EmbeddingRecord


class QdrantStorage:
    """Handles storing embeddings in Qdrant Cloud."""

    def __init__(self, config: ProcessingConfig):
        """
        Initialize the Qdrant storage with configuration.

        Args:
            config: Processing configuration with Qdrant credentials
        """
        self.config = config
        self.client = QdrantClient(
            url=config.qdrant_url,
            api_key=config.qdrant_api_key,
            https=True
        )
        self.collection_name = "content_embeddings"
        self.logger = logging.getLogger(__name__)

        # Initialize the collection if it doesn't exist
        self._initialize_collection()

    def _initialize_collection(self):
        """Initialize the Qdrant collection for storing embeddings."""
        try:
            # Check if collection exists
            collections = self.client.get_collections()
            collection_exists = any(col.name == self.collection_name for col in collections.collections)

            if not collection_exists:
                # Create collection with appropriate vector size (we'll assume Cohere's default)
                # For embed-english-v3.0, the default size is 1024
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=1024,  # Cohere's default embedding size
                        distance=models.Distance.COSINE
                    )
                )
                self.logger.info(f"Created Qdrant collection: {self.collection_name}")
            else:
                self.logger.info(f"Qdrant collection exists: {self.collection_name}")

        except Exception as e:
            self.logger.error(f"Error initializing Qdrant collection: {str(e)}")
            raise StorageException(f"Failed to initialize Qdrant collection: {str(e)}")

    def store_embeddings(self, embedding_records: List[EmbeddingRecord]) -> bool:
        """
        Store a list of embedding records in Qdrant.

        Args:
            embedding_records: List of EmbeddingRecord objects to store

        Returns:
            True if storage was successful, False otherwise
        """
        if not embedding_records:
            self.logger.info("No embeddings to store")
            return True

        try:
            # Prepare points for insertion
            points = []
            for i, record in enumerate(embedding_records):
                point = PointStruct(
                    id=record.id,
                    vector=record.vector,
                    payload={
                        "source_url": record.metadata.get("source_url"),
                        "title": record.metadata.get("title"),
                        "section": record.metadata.get("section", ""),
                        "chunk_index": record.metadata.get("chunk_index", 0),
                        "original_id": record.metadata.get("id", ""),
                        "created_at": record.created_at.isoformat(),
                        "content": record.metadata.get("content", "")  # Add content to payload if available
                    }
                )
                points.append(point)

            # Upload points to Qdrant
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )

            self.logger.info(f"Successfully stored {len(embedding_records)} embeddings in Qdrant")
            return True

        except Exception as e:
            self.logger.error(f"Error storing embeddings in Qdrant: {str(e)}")
            raise StorageException(f"Failed to store embeddings in Qdrant: {str(e)}")

    def store_single_embedding(self, embedding_record: EmbeddingRecord) -> bool:
        """
        Store a single embedding record in Qdrant.

        Args:
            embedding_record: EmbeddingRecord object to store

        Returns:
            True if storage was successful, False otherwise
        """
        return self.store_embeddings([embedding_record])

    def search_embeddings(self, query_vector: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar embeddings in Qdrant.

        Args:
            query_vector: Vector to search for similar embeddings
            limit: Maximum number of results to return

        Returns:
            List of matching points with payload data
        """
        try:
            # Using the correct Qdrant client search method: query_points
            search_response = self.client.query_points(
                collection_name=self.collection_name,
                query=query_vector,
                limit=limit
            )

            # The query_points method returns a Response object with points
            # Let's handle the response properly
            try:
                # Check if it's a tuple response (common in older versions)
                if isinstance(search_response, tuple):
                    results, _ = search_response
                else:
                    # For newer versions, it might return a Response object
                    results = search_response
            except ValueError:
                # If it's not a tuple, use the response directly
                results = search_response

            # Extract relevant information from results
            matches = []

            # Check the structure of the response - it's likely a QueryResponse object
            if hasattr(search_response, 'points'):
                # Newer version returns a QueryResponse object with a 'points' attribute
                for result in search_response.points:
                    matches.append({
                        "id": result.id if hasattr(result, 'id') else getattr(result, 'point_id', None),
                        "score": getattr(result, 'score', None),
                        "payload": getattr(result, 'payload', {}) if hasattr(result, 'payload') else getattr(result, 'payload', {}),
                        "vector": getattr(result, 'vector', None)
                    })
            elif hasattr(results, '__iter__') and not isinstance(results, (str, bytes)):
                # If it's iterable (fallback)
                for result in results:
                    matches.append({
                        "id": result.id if hasattr(result, 'id') else getattr(result, 'point_id', None),
                        "score": result.score if hasattr(result, 'score') else getattr(result, 'score', None),
                        "payload": result.payload if hasattr(result, 'payload') else getattr(result, 'payload', {}),
                        "vector": result.vector if hasattr(result, 'vector') else getattr(result, 'vector', None)
                    })
            else:
                # Handle other possible structures
                if hasattr(results, 'points'):
                    for result in results.points:
                        matches.append({
                            "id": result.id if hasattr(result, 'id') else getattr(result, 'point_id', None),
                            "score": result.score if hasattr(result, 'score') else getattr(result, 'score', None),
                            "payload": result.payload if hasattr(result, 'payload') else getattr(result, 'payload', {}),
                            "vector": result.vector if hasattr(result, 'vector') else getattr(result, 'vector', None)
                        })

            self.logger.info(f"Search returned {len(matches)} results")
            return matches

        except AttributeError as e:
            # Handle case where query_points method doesn't exist
            self.logger.error(f"Qdrant client does not have query_points method: {str(e)}")
            # Try alternative method names that might exist
            try:
                # Alternative: search method
                results = self.client.search(
                    collection_name=self.collection_name,
                    query_vector=query_vector,
                    limit=limit
                )

                # Extract relevant information from results
                matches = []
                for result in results:
                    matches.append({
                        "id": result.id,
                        "score": result.score,
                        "payload": result.payload,
                        "vector": result.vector if result.vector else None
                    })

                self.logger.info(f"Search returned {len(matches)} results")
                return matches
            except AttributeError:
                # Try another alternative: search_points method
                try:
                    results = self.client.search_points(
                        collection_name=self.collection_name,
                        query_vector=query_vector,
                        limit=limit
                    )

                    # Extract relevant information from results
                    matches = []
                    for result in results:
                        matches.append({
                            "id": result.id,
                            "score": result.score,
                            "payload": result.payload,
                            "vector": result.vector if result.vector else None
                        })

                    self.logger.info(f"Search returned {len(matches)} results")
                    return matches
                except AttributeError:
                    self.logger.error("Qdrant client does not have query_points, search, or search_points methods")
                    raise StorageException("Qdrant client does not have search functionality")
        except Exception as e:
            self.logger.error(f"Error searching embeddings in Qdrant: {str(e)}")
            raise StorageException(f"Failed to search embeddings in Qdrant: {str(e)}")

    def validate_embedding_dimensions(self, embeddings: List[EmbeddingRecord]) -> bool:
        """
        Validate that all embeddings have the correct dimension for the collection.

        Args:
            embeddings: List of EmbeddingRecord objects to validate

        Returns:
            True if all embeddings have correct dimensions, False otherwise
        """
        if not embeddings:
            return True

        # For Cohere embed-english-v3.0, the expected size is 1024
        expected_size = 1024

        for record in embeddings:
            if len(record.vector) != expected_size:
                self.logger.error(f"Embedding vector has incorrect size: {len(record.vector)}, expected: {expected_size}")
                return False

        return True

    def get_collection_info(self) -> Dict[str, Any]:
        """
        Get information about the collection.

        Returns:
            Dictionary with collection information
        """
        try:
            collection_info = self.client.get_collection(self.collection_name)
            return {
                "name": collection_info.config.params.vectors.size,
                "vector_size": collection_info.config.params.vectors.size,
                "distance": collection_info.config.params.vectors.distance,
                "point_count": collection_info.points_count
            }
        except Exception as e:
            self.logger.error(f"Error getting collection info: {str(e)}")
            raise StorageException(f"Failed to get collection info: {str(e)}")

    def close(self):
        """Close the Qdrant client connection."""
        try:
            self.client.close()
            self.logger.info("Qdrant client connection closed")
        except Exception as e:
            self.logger.error(f"Error closing Qdrant client: {str(e)}")