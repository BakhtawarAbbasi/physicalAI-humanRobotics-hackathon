#!/usr/bin/env python3
"""
Test script to verify the RAG agent functionality.
"""

import asyncio
from api import RAGAgentAPI


async def test_agent_functionality():
    """Test the RAG agent functionality."""
    print("Testing RAG Agent functionality...")

    # Create the agent
    agent = RAGAgentAPI()

    # Test a query
    test_query = "What is Gazebo physics simulation?"
    print(f"Testing query: '{test_query}'")

    try:
        response = await agent.query_rag_agent(test_query, top_k=3)

        print(f"Query successful: {response.success}")
        print(f"Answer length: {len(response.answer)} characters")
        print(f"Sources found: {len(response.sources)}")
        print(f"Chunks retrieved: {len(response.retrieved_chunks)}")

        if response.success:
            print("✅ RAG Agent is working correctly!")
            print(f"Sample answer preview: {response.answer[:100]}...")

            if response.sources:
                print(f"First source: {response.sources[0]}")

            if response.retrieved_chunks:
                first_chunk = response.retrieved_chunks[0]
                print(f"First chunk score: {first_chunk.score}")
                print(f"First chunk source: {first_chunk.source_url}")
                print(f"First chunk content preview: {first_chunk.content[:100]}...")
        else:
            print(f"❌ Query failed with error: {response.error_message}")

    except Exception as e:
        print(f"❌ Error during agent test: {str(e)}")
        import traceback
        traceback.print_exc()

    finally:
        # Clean up resources if needed
        pass


if __name__ == "__main__":
    asyncio.run(test_agent_functionality())