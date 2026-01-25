#!/usr/bin/env python3
"""
Comprehensive test script to verify the complete RAG pipeline functionality.
Tests all components: ingestion, storage, retrieval, and API endpoints.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the backend directory to the path so we can import our modules
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from config.settings import ProcessingConfig
from src.crawler.crawler_service import CrawlerService
from src.chunker.chunker_service import ChunkerService
from src.embedding.embedding_service import EmbeddingService
from src.storage.qdrant_storage import QdrantStorage
from src.pipeline.ingestion_pipeline import IngestionPipeline
from api import RAGAgentAPI
import httpx
import time


async def test_pipeline_components():
    """Test individual pipeline components."""
    print("[TEST] Testing individual pipeline components...")

    # Load configuration
    config = ProcessingConfig()
    print(f"   [OK] Configuration loaded: {config.chunk_size} chars, {config.chunk_overlap} overlap")

    # Test crawler service
    crawler = CrawlerService(config)
    print("   [OK] Crawler service initialized")

    # Test chunker service
    chunker = ChunkerService(config)
    print("   [OK] Chunker service initialized")

    # Test embedding service
    embedding_service = EmbeddingService(config)
    print("   [OK] Embedding service initialized")

    # Test Qdrant storage
    storage = QdrantStorage(config)
    print("   [OK] Qdrant storage initialized")

    # Test ingestion pipeline
    pipeline = IngestionPipeline(config)
    print("   [OK] Ingestion pipeline initialized")

    return True


async def test_ingestion_pipeline():
    """Test the complete ingestion pipeline with sample URLs."""
    print("\n[TEST] Testing ingestion pipeline...")

    config = ProcessingConfig()
    pipeline = IngestionPipeline(config)

    # Test with a few sample URLs from the deployed site
    test_urls = [
        "https://physical-ai-human-robotics-hackatho-ebon.vercel.app/",
        "https://physical-ai-human-robotics-hackatho-ebon.vercel.app/docs/module-01",
    ]

    print(f"   Testing ingestion of {len(test_urls)} URLs...")

    try:
        # Use the correct method to run the pipeline
        result = await pipeline.run_pipeline_with_validation(urls=test_urls, max_depth=1)
        print(f"   [OK] Ingestion pipeline completed successfully")
        print(f"   Job status: {result.status}")
        print(f"   URLs processed: {len(result.urls)}")
        print(f"   Processed count: {result.processed_count}")
        print(f"   Failed count: {result.failed_count}")

        return result.status == 'completed'

    except Exception as e:
        print(f"   [ERROR] Error during ingestion: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_qdrant_storage():
    """Test Qdrant storage functionality."""
    print("\n[TEST] Testing Qdrant storage...")

    config = ProcessingConfig()
    storage = QdrantStorage(config)

    try:
        # Test collection exists and get info
        collection_info = storage.get_collection_info()
        count = collection_info.get('point_count', 0)
        print(f"   [OK] Collection exists, current count: {count} vectors")

        # Test search functionality
        if count > 0:
            # Search for a generic term to test retrieval
            # We'll need to generate a query vector first using Cohere
            from cohere import Client
            from config.settings import ProcessingConfig as Config
            config_obj = Config()
            cohere_client = Client(api_key=config_obj.cohere_api_key)

            query_embedding = cohere_client.embed(
                texts=["robotics"],
                model="embed-english-v3.0",
                input_type="search_query"
            ).embeddings[0]

            results = storage.search_embeddings(query_vector=query_embedding, limit=3)
            print(f"   [OK] Search successful, retrieved {len(results)} results")
            if results:
                print(f"   First result score: {results[0]['score']:.4f}")
        else:
            print("   [WARN] No vectors in collection yet, ingestion may be needed")

        return True

    except Exception as e:
        print(f"   [ERROR] Error testing Qdrant: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_rag_agent():
    """Test the RAG agent functionality."""
    print("\n[TEST] Testing RAG agent...")

    try:
        agent = RAGAgentAPI()
        print("   [OK] RAG Agent initialized")

        # Test a query
        query = "What is Gazebo physics simulation?"
        print(f"   Query: {query}")

        result = await agent.query_rag_agent(query, top_k=3)

        print(f"   [OK] Query processed successfully")
        print(f"   Retrieved chunks: {len(result.retrieved_chunks)}")
        print(f"   Sources found: {len(result.sources)}")
        print(f"   Success: {result.success}")

        if result.success:
            print(f"   Answer preview: {result.answer[:100]}...")

            if result.sources:
                print(f"   First source: {result.sources[0]}")

            if result.retrieved_chunks:
                print(f"   First chunk score: {result.retrieved_chunks[0].score}")
        else:
            print(f"   Error message: {result.error_message}")

        return result.success

    except Exception as e:
        print(f"   [ERROR] Error testing RAG agent: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_api_endpoints():
    """Test the FastAPI endpoints."""
    print("\n[TEST] Testing FastAPI endpoints...")

    base_url = "http://localhost:8000"

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Test health endpoint
            print(f"   Testing health endpoint: {base_url}/health")
            response = await client.get(f"{base_url}/health")
            print(f"   Health status: {response.status_code}")
            if response.status_code == 200:
                health_data = response.json()
                print(f"   Health response: {health_data}")
                print("   [OK] Health endpoint working")
            else:
                print("   [ERROR] Health endpoint failed")
                return False

            # Test query endpoint
            print(f"   Testing query endpoint: {base_url}/query")
            query_data = {
                "query": "What is Gazebo physics simulation?",
                "top_k": 3
            }

            response = await client.post(
                f"{base_url}/query",
                json=query_data,
                timeout=30.0
            )

            print(f"   Query status: {response.status_code}")
            if response.status_code == 200:
                query_result = response.json()
                print(f"   Retrieved chunks: {len(query_result.get('retrieved_chunks', []))}")
                print(f"   Sources found: {len(query_result.get('sources', []))}")
                print(f"   Success: {query_result.get('success', False)}")
                print("   [OK] Query endpoint working")

                # Show first few characters of response
                answer = query_result.get('answer', '')
                if answer:
                    print(f"   Response preview: {answer[:100]}...")
            else:
                print("   [ERROR] Query endpoint failed")
                print(f"   Error: {response.text}")
                return False

        return True

    except Exception as e:
        print(f"   [ERROR] Error testing API endpoints: {str(e)}")
        print("   Note: If server isn't running, start it with: python -m uvicorn api:app --host 0.0.0.0 --port 8000")
        return False


async def main():
    """Main test function."""
    print("Starting comprehensive RAG pipeline verification...")
    print("=" * 60)

    start_time = time.time()

    # Test individual components
    components_ok = await test_pipeline_components()

    # Test Qdrant storage
    storage_ok = await test_qdrant_storage()

    # Test ingestion pipeline
    ingestion_ok = await test_ingestion_pipeline()

    # Test RAG agent
    agent_ok = await test_rag_agent()

    # Test API endpoints (if server is running)
    api_ok = await test_api_endpoints()

    total_time = time.time() - start_time

    print("\n" + "=" * 60)
    print("TEST RESULTS SUMMARY:")
    print(f"   Components: {'PASS' if components_ok else 'FAIL'}")
    print(f"   Storage:    {'PASS' if storage_ok else 'FAIL'}")
    print(f"   Ingestion:  {'PASS' if ingestion_ok else 'FAIL'}")
    print(f"   RAG Agent:  {'PASS' if agent_ok else 'FAIL'}")
    print(f"   API:        {'PASS' if api_ok else 'FAIL'}")

    all_passed = all([components_ok, storage_ok, ingestion_ok, agent_ok, api_ok])
    print(f"\n   Overall: {'ALL TESTS PASSED!' if all_passed else 'SOME TESTS FAILED'}")
    print(f"   Total time: {total_time:.2f} seconds")

    return all_passed


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)