#!/usr/bin/env python3
"""
RAG Retrieval Validation Script

This script connects to Qdrant and validates the retrieval pipeline by:
- Connecting to Qdrant and loading existing vector collections
- Accepting a test query and performing top-k similarity search
- Validating results using returned text, metadata, and source URLs
"""

import argparse
import logging
from typing import List, Dict, Any, Optional
import sys

from config.settings import ProcessingConfig
from qdrant_client import QdrantClient
from qdrant_client.http import models
from cohere import Client as CohereClient

from src.storage.qdrant_storage import QdrantStorage


class RAGRetriever:
    """Handles retrieval operations for the RAG system."""

    def __init__(self):
        """Initialize the retriever with configuration."""
        self.config = ProcessingConfig()
        self.qdrant_storage = QdrantStorage(self.config)
        self.cohere_client = CohereClient(self.config.cohere_api_key)
        self.collection_name = "content_embeddings"
        self.logger = logging.getLogger(__name__)

        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

    def connect_and_load_collections(self) -> Dict[str, Any]:
        """
        Connect to Qdrant and load existing vector collections.

        Returns:
            Dictionary with collection information
        """
        try:
            self.logger.info("Connecting to Qdrant...")

            # Get collection info using the storage class
            collection_info = self.qdrant_storage.get_collection_info()

            info = {
                "name": self.collection_name,
                "vector_size": collection_info['vector_size'],
                "distance": collection_info['distance'],
                "point_count": collection_info['point_count'],
                "vectors_count": 'N/A'  # Not available in the current method
            }

            self.logger.info(f"Collection: {info['name']}")
            self.logger.info(f"Vector size: {info['vector_size']}")
            self.logger.info(f"Distance: {info['distance']}")
            self.logger.info(f"Point count: {info['point_count']}")

            return info

        except Exception as e:
            self.logger.error(f"Error connecting to Qdrant: {str(e)}")
            raise

    def search_similar_content(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Perform top-k similarity search for a given query.

        Args:
            query: The query string to search for
            top_k: Number of top results to retrieve

        Returns:
            List of retrieved chunks with content, metadata, and scores
        """
        try:
            self.logger.info(f"Processing query: '{query}'")
            self.logger.info(f"Retrieving top-{top_k} similar content...")

            # Generate embedding for the query
            response = self.cohere_client.embed(
                texts=[query],
                model="embed-english-v3.0",
                input_type="search_query"
            )

            query_embedding = response.embeddings[0] if response.embeddings else None

            if not query_embedding:
                raise Exception("Failed to generate embedding for query")

            # Search in Qdrant using the storage class
            search_results = self.qdrant_storage.search_embeddings(
                query_vector=query_embedding,
                limit=top_k
            )

            # Process results
            retrieved_chunks = []
            for result in search_results:
                payload = result["payload"]
                chunk = {
                    "content": payload.get("content", ""),
                    "source_url": payload.get("source_url", ""),
                    "title": payload.get("title", ""),
                    "section": payload.get("section", ""),
                    "chunk_index": payload.get("chunk_index", 0),
                    "score": result["score"],
                    "id": result["id"]
                }
                retrieved_chunks.append(chunk)

            self.logger.info(f"Retrieved {len(retrieved_chunks)} chunks for query: '{query}'")
            return retrieved_chunks

        except Exception as e:
            self.logger.error(f"Error performing similarity search: {str(e)}")
            raise

    def validate_results(self, retrieved_chunks: List[Dict[str, Any]], query: str) -> Dict[str, Any]:
        """
        Validate results using returned text, metadata, and source URLs.

        Args:
            retrieved_chunks: List of retrieved chunks to validate
            query: Original query for context

        Returns:
            Dictionary with validation results
        """
        try:
            self.logger.info("Validating retrieved results...")

            if not retrieved_chunks:
                return {
                    "is_valid": False,
                    "metadata_accuracy": 0.0,
                    "content_accuracy": 0.0,
                    "errors": ["No chunks retrieved for validation"],
                    "warnings": [],
                    "total_chunks": 0,
                    "valid_chunks": 0
                }

            total_chunks = len(retrieved_chunks)
            valid_chunks = 0
            errors = []
            warnings = []

            for chunk in retrieved_chunks:
                chunk_errors = []
                chunk_warnings = []

                # Validate metadata
                if not chunk.get("source_url"):
                    chunk_errors.append("Missing source_url")
                if not chunk.get("title"):
                    chunk_errors.append("Missing title")
                if chunk.get("chunk_index") is None:
                    chunk_warnings.append("Missing chunk_index")

                # Validate content
                if not chunk.get("content") or len(chunk.get("content", "").strip()) == 0:
                    chunk_errors.append("Empty content")

                # Validate score
                if chunk.get("score") is None:
                    chunk_errors.append("Missing score")

                if chunk_errors:
                    errors.extend([f"Chunk {chunk.get('id', 'unknown')}: {err}" for err in chunk_errors])
                if chunk_warnings:
                    warnings.extend([f"Chunk {chunk.get('id', 'unknown')}: {warn}" for warn in chunk_warnings])

                if not chunk_errors:
                    valid_chunks += 1

            metadata_accuracy = (valid_chunks / total_chunks) * 100 if total_chunks > 0 else 0
            content_accuracy = (valid_chunks / total_chunks) * 100 if total_chunks > 0 else 0

            validation_result = {
                "is_valid": len(errors) == 0,
                "metadata_accuracy": metadata_accuracy,
                "content_accuracy": content_accuracy,
                "errors": errors,
                "warnings": warnings,
                "total_chunks": total_chunks,
                "valid_chunks": valid_chunks,
                "query": query
            }

            self.logger.info(f"Validation completed: {valid_chunks}/{total_chunks} chunks valid")
            self.logger.info(f"Metadata accuracy: {metadata_accuracy:.1f}%")

            return validation_result

        except Exception as e:
            self.logger.error(f"Error validating results: {str(e)}")
            return {
                "is_valid": False,
                "metadata_accuracy": 0.0,
                "content_accuracy": 0.0,
                "errors": [f"Validation error: {str(e)}"],
                "warnings": [],
                "total_chunks": 0,
                "valid_chunks": 0,
                "query": query
            }

    def run_validation(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        """
        Run complete validation of the RAG retrieval pipeline.

        Args:
            query: Query string to test
            top_k: Number of top results to retrieve

        Returns:
            Dictionary with complete validation results
        """
        try:
            self.logger.info("Starting RAG retrieval validation...")

            # Step 1: Connect and load collections
            collection_info = self.connect_and_load_collections()

            # Step 2: Perform similarity search
            retrieved_chunks = self.search_similar_content(query, top_k)

            # Step 3: Validate results
            validation_result = self.validate_results(retrieved_chunks, query)

            # Combine all results
            result = {
                "collection_info": collection_info,
                "query": query,
                "top_k": top_k,
                "retrieved_chunks": retrieved_chunks,
                "validation": validation_result
            }

            return result

        except Exception as e:
            self.logger.error(f"Error during validation: {str(e)}")
            raise

    def close(self):
        """Close connections."""
        try:
            self.qdrant_storage.close()
            self.logger.info("Qdrant client connection closed")
        except Exception as e:
            self.logger.error(f"Error closing Qdrant client: {str(e)}")


def main():
    """Main function to run the RAG retrieval validation."""
    parser = argparse.ArgumentParser(description="RAG Retrieval Validation")
    parser.add_argument("--query", type=str, help="Query to test",
                        default="What is Gazebo physics simulation?")
    parser.add_argument("--top-k", type=int, default=5, help="Number of top results to retrieve")

    args = parser.parse_args()

    retriever = RAGRetriever()

    try:
        results = retriever.run_validation(args.query, args.top_k)

        print("\n" + "="*70)
        print("RAG RETRIEVAL VALIDATION RESULTS")
        print("="*70)
        print(f"Query: {results['query']}")
        print(f"Top-K: {results['top_k']}")
        print(f"Collection: {results['collection_info']['name']}")
        print(f"Vector Count: {results['collection_info']['point_count']}")
        print("-" * 70)
        print(f"Retrieved Chunks: {len(results['retrieved_chunks'])}")
        print(f"Valid Chunks: {results['validation']['valid_chunks']}")
        print(f"Metadata Accuracy: {results['validation']['metadata_accuracy']:.1f}%")
        print(f"Validation Passed: {'YES' if results['validation']['is_valid'] else 'NO'}")
        print("-" * 70)

        if results['validation']['errors']:
            print("ERRORS:")
            for error in results['validation']['errors']:
                print(f"  - {error}")
            print()

        if results['validation']['warnings']:
            print("WARNINGS:")
            for warning in results['validation']['warnings']:
                print(f"  - {warning}")
            print()

        # Show top 3 results
        print("TOP RESULTS:")
        for i, chunk in enumerate(results['retrieved_chunks'][:3], 1):
            print(f"\n{i}. Score: {chunk['score']:.3f}")
            print(f"   Source: {chunk['source_url']}")
            print(f"   Title: {chunk['title']}")
            # Sanitize content to avoid Unicode encoding issues in output
            content_preview = chunk['content'][:100].encode('utf-8', errors='ignore').decode('utf-8')
            print(f"   Content Preview: {content_preview}...")
            print()

        print("="*70)
        if results['validation']['is_valid']:
            print("OK RAG retrieval pipeline validation successful!")
            print("The system can successfully retrieve relevant content from Qdrant.")
        else:
            print("NO RAG retrieval pipeline validation failed!")
            print("Some components need attention before the system is ready.")
        print("="*70)

    except Exception as e:
        print(f"NO Error during validation: {str(e)}")
        sys.exit(1)
    finally:
        retriever.close()


if __name__ == "__main__":
    main()