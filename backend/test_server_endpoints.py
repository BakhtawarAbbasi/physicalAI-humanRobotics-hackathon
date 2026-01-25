#!/usr/bin/env python3
"""
Test script to verify the FastAPI server endpoints are working correctly.
"""

import asyncio
import httpx
import json


async def test_api_endpoints():
    """Test the FastAPI endpoints."""
    print("Testing FastAPI endpoints...")

    base_url = "http://localhost:8001"  # Using port 8001 where server is running

    print(f"Base URL: {base_url}")

    # Test health endpoint
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            print(f"\n1. Testing health endpoint: {base_url}/health")
            response = await client.get(f"{base_url}/health")
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                health_data = response.json()
                print(f"   Response: {health_data}")
                print("   ✅ Health endpoint working")
            else:
                print("   ❌ Health endpoint failed")

            # Test docs endpoint
            print(f"\n2. Testing docs endpoint: {base_url}/docs")
            response = await client.get(f"{base_url}/docs")
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                print("   ✅ Docs endpoint working (Swagger UI available)")
            else:
                print("   ❌ Docs endpoint failed")

            # Test query endpoint with a sample query
            print(f"\n3. Testing query endpoint: {base_url}/query")
            query_data = {
                "query": "What is Gazebo physics simulation?",
                "top_k": 3
            }

            response = await client.post(
                f"{base_url}/query",
                json=query_data,
                timeout=30.0
            )

            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                query_result = response.json()
                print(f"   Retrieved chunks: {len(query_result.get('retrieved_chunks', []))}")
                print(f"   Sources found: {len(query_result.get('sources', []))}")
                print(f"   Success: {query_result.get('success', False)}")
                print("   ✅ Query endpoint working")

                # Show first few characters of response
                answer = query_result.get('answer', '')
                if answer:
                    print(f"   Response preview: {answer[:100]}...")
            else:
                print("   ❌ Query endpoint failed")
                print(f"   Error: {response.text}")

    except Exception as e:
        print(f"   ❌ Error testing endpoints: {str(e)}")
        print("   Note: If server isn't running, start it with: python -m uvicorn api:app --host 0.0.0.0 --port 8001")


if __name__ == "__main__":
    asyncio.run(test_api_endpoints())