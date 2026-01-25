#!/usr/bin/env python3
"""
Validation script for RAG retrieval pipeline.
This script validates that stored embeddings in Qdrant can be retrieved correctly.
"""

import asyncio
from typing import List, Dict, Any
import logging

from config.settings import ProcessingConfig
from qdrant_client import QdrantClient
from qdrant_client.http import models
from cohere import Client as CohereClient


class RAGRetrievalValidator:
    """Validates the RAG retrieval pipeline by testing Qdrant connections and retrieval functionality."""

    def __init__(self):
        """Initialize the validator with configuration."""
        self.config = ProcessingConfig()
        self.qdrant_client = QdrantClient(
            url=self.config.qdrant_url,
            api_key=self.config.qdrant_api_key,
            https=True
        )
        self.cohere_client = CohereClient(self.config.cohere_api_key)
        self.collection_name = "content_embeddings"
        self.logger = logging.getLogger(__name__)

        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

    def validate_qdrant_connection(self) -> bool:
        """
        Validate connection to Qdrant and check stored vectors.

        Returns:
            True if connection and vector loading are successful, False otherwise
        """
        try:
            self.logger.info("Validating Qdrant connection...")

            # Get collection info
            collection_info = self.qdrant_client.get_collection(self.collection_name)

            self.logger.info(f"Collection: {self.collection_name}")
            self.logger.info(f"Vector size: {collection_info.config.params.vectors.size}")
            self.logger.info(f"Distance: {collection_info.config.params.vectors.distance}")
            self.logger.info(f"Point count: {collection_info.points_count}")

            # Check if we have vectors stored
            if collection_info.points_count == 0:
                self.logger.error("No vectors found in collection")
                return False

            self.logger.info("Qdrant connection validated successfully")
            return True

        except Exception as e:
            self.logger.error(f"Error validating Qdrant connection: {str(e)}")
            return False

    def execute_test_queries(self, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Execute test queries against stored embeddings to retrieve relevant text chunks.

        Args:
            top_k: Number of top results to retrieve

        Returns:
            List of retrieved text chunks with metadata
        """
        try:
            self.logger.info(f"Executing test queries to retrieve top-{top_k} relevant chunks...")

            # Sample test queries related to the documentation content
            test_queries = [
                "What is Gazebo physics simulation?",
                "How does ROS2 work with humanoid robots?",
                "Explain URDF modeling for robots",
                "What are Isaac Sim and Unity Digital Twin?",
                "How does Nav2 work for humanoid navigation?"
            ]

            all_results = []

            for i, query in enumerate(test_queries):
                self.logger.info(f"Processing query {i+1}/{len(test_queries)}: '{query}'")

                # Generate embedding for the query
                response = self.cohere_client.embed(
                    texts=[query],
                    model="embed-english-v3.0",
                    input_type="search_query"
                )

                query_embedding = response.embeddings[0] if response.embeddings else None

                if not query_embedding:
                    self.logger.error(f"Failed to generate embedding for query: {query}")
                    continue

                # Search in Qdrant
                search_results = self.qdrant_client.search(
                    collection_name=self.collection_name,
                    query_vector=query_embedding,
                    limit=top_k
                )

                # Process results
                for result in search_results:
                    payload = result.payload
                    retrieved_chunk = {
                        "query": query,
                        "content": payload.get("content", "")[:200] + "..." if len(payload.get("content", "")) > 200 else payload.get("content", ""),
                        "source_url": payload.get("source_url", ""),
                        "title": payload.get("title", ""),
                        "score": result.score,
                        "chunk_index": payload.get("chunk_index", 0)
                    }
                    all_results.append(retrieved_chunk)

                    self.logger.info(f"  - Score: {result.score:.3f}, URL: {payload.get('source_url', '')[:50]}...")

            self.logger.info(f"Retrieved {len(all_results)} total chunks from {len(test_queries)} queries")
            return all_results

        except Exception as e:
            self.logger.error(f"Error executing test queries: {str(e)}")
            return []

    def validate_metadata_accuracy(self, retrieved_chunks: List[Dict[str, Any]]) -> bool:
        """
        Validate that retrieved content matches source URLs and metadata.

        Args:
            retrieved_chunks: List of retrieved chunks to validate

        Returns:
            True if metadata accuracy is validated, False otherwise
        """
        try:
            self.logger.info("Validating content metadata accuracy...")

            if not retrieved_chunks:
                self.logger.error("No retrieved chunks to validate")
                return False

            valid_chunks = 0
            total_chunks = len(retrieved_chunks)

            for chunk in retrieved_chunks[:10]:  # Check first 10 as sample
                source_url = chunk.get("source_url", "")
                title = chunk.get("title", "")

                if source_url and title:
                    valid_chunks += 1
                    self.logger.debug(f"Valid chunk: {source_url} - {title[:50]}...")
                else:
                    self.logger.warning(f"Missing metadata in chunk: {chunk}")

            accuracy_rate = (valid_chunks / min(10, total_chunks)) * 100 if total_chunks > 0 else 0
            self.logger.info(f"Metadata validation: {valid_chunks}/{min(10, total_chunks)} chunks have complete metadata ({accuracy_rate:.1f}%)")

            # Check if accuracy meets threshold (95% as specified in requirements)
            if accuracy_rate >= 95:
                self.logger.info("Metadata accuracy validation passed")
                return True
            else:
                self.logger.warning("Metadata accuracy validation failed - below 95% threshold")
                return False

        except Exception as e:
            self.logger.error(f"Error validating metadata accuracy: {str(e)}")
            return False

    def run_validation(self) -> Dict[str, Any]:
        """
        Run complete validation of the RAG retrieval pipeline.

        Returns:
            Dictionary with validation results
        """
        self.logger.info("Starting RAG retrieval pipeline validation...")

        results = {
            "qdrant_connection": False,
            "vector_count": 0,
            "test_queries_executed": False,
            "retrieved_chunks_count": 0,
            "metadata_accuracy_validated": False,
            "all_tests_passed": False,
            "details": {}
        }

        # Step 1: Validate Qdrant connection and vector loading
        self.logger.info("Step 1: Validating Qdrant connection and vector loading")
        results["qdrant_connection"] = self.validate_qdrant_connection()

        if results["qdrant_connection"]:
            collection_info = self.qdrant_client.get_collection(self.collection_name)
            results["vector_count"] = collection_info.points_count
            self.logger.info(f"Found {results['vector_count']} vectors in collection")
        else:
            self.logger.error("Qdrant connection validation failed - stopping validation")
            return results

        # Step 2: Execute test queries to retrieve relevant text chunks
        self.logger.info("Step 2: Executing test queries for top-k retrieval")
        retrieved_chunks = self.execute_test_queries(top_k=3)
        results["retrieved_chunks_count"] = len(retrieved_chunks)
        results["test_queries_executed"] = len(retrieved_chunks) > 0

        if not results["test_queries_executed"]:
            self.logger.error("Test query execution failed - no chunks retrieved")
            return results

        # Step 3: Validate content metadata accuracy
        self.logger.info("Step 3: Validating content metadata accuracy")
        results["metadata_accuracy_validated"] = self.validate_metadata_accuracy(retrieved_chunks)

        # Overall validation result
        results["all_tests_passed"] = (
            results["qdrant_connection"] and
            results["test_queries_executed"] and
            results["metadata_accuracy_validated"]
        )

        self.logger.info(f"Validation completed. All tests passed: {results['all_tests_passed']}")

        return results

    def close(self):
        """Close connections."""
        try:
            self.qdrant_client.close()
            self.logger.info("Qdrant client connection closed")
        except Exception as e:
            self.logger.error(f"Error closing Qdrant client: {str(e)}")


def main():
    """Main function to run the RAG retrieval validation."""
    validator = RAGRetrievalValidator()

    try:
        results = validator.run_validation()

        print("\n" + "="*60)
        print("RAG RETRIEVAL PIPELINE VALIDATION RESULTS")
        print("="*60)
        print(f"Qdrant Connection: {'OK PASS' if results['qdrant_connection'] else 'NO FAIL'}")
        print(f"Vector Count: {results['vector_count']}")
        print(f"Test Queries Executed: {'OK PASS' if results['test_queries_executed'] else 'NO FAIL'}")
        print(f"Retrieved Chunks: {results['retrieved_chunks_count']}")
        print(f"Metadata Accuracy: {'OK PASS' if results['metadata_accuracy_validated'] else 'NO FAIL'}")
        print("-" * 60)
        print(f"OVERALL: {'OK ALL TESTS PASSED' if results['all_tests_passed'] else 'NO SOME TESTS FAILED'}")
        print("="*60)

        if results['all_tests_passed']:
            print("\nOK RAG retrieval pipeline validation successful!")
            print("The system can successfully retrieve relevant content from Qdrant.")
        else:
            print("\nNO RAG retrieval pipeline validation failed!")
            print("Some components need attention before the system is ready.")

    except Exception as e:
        print(f"NO Error during validation: {str(e)}")
    finally:
        validator.close()


if __name__ == "__main__":
    main()