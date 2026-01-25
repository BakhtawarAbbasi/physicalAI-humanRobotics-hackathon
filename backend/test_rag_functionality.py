#!/usr/bin/env python3
"""
Test script to verify the RAG agent functionality.
"""

import asyncio
from api import RAGAgentAPI


async def test_rag_agent():
    """Test the RAG agent functionality."""
    print("Testing RAG Agent functionality...")

    # Create the agent
    agent = RAGAgentAPI()

    # Test a query
    query = "What is Gazebo physics simulation?"
    print(f"Query: {query}")

    try:
        result = await agent.query_rag_agent(query, top_k=3)

        print(f"✅ Query processed successfully")
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

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_rag_agent())