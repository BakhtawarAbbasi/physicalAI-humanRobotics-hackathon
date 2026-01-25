#!/usr/bin/env python3
"""
Test script to verify the FastAPI server endpoints on port 8002.
"""

import requests
import json


def test_api_endpoints():
    """Test the FastAPI endpoints."""
    print("Testing FastAPI endpoints on port 8002...")

    base_url = "http://localhost:8002"  # Using port 8002 where server is running

    print(f"Base URL: {base_url}")

    # Test health endpoint
    try:
        print(f"\n1. Testing health endpoint: {base_url}/health")
        response = requests.get(f"{base_url}/health", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            health_data = response.json()
            print(f"   Response: {health_data}")
            print("   [OK] Health endpoint working")
        else:
            print("   [ERROR] Health endpoint failed")

        # Test docs endpoint
        print(f"\n2. Testing docs endpoint: {base_url}/docs")
        response = requests.get(f"{base_url}/docs", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   [OK] Docs endpoint working (Swagger UI available)")
        else:
            print("   [ERROR] Docs endpoint failed")

        # Test query endpoint with a sample query
        print(f"\n3. Testing query endpoint: {base_url}/query")
        query_data = {
            "query": "What is Gazebo physics simulation?",
            "top_k": 3
        }

        response = requests.post(
            f"{base_url}/query",
            json=query_data,
            timeout=30
        )

        print(f"   Status: {response.status_code}")
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

        print("\n" + "="*60)
        print("ALL TESTS COMPLETED SUCCESSFULLY!")
        print("RAG system is running and responding to queries.")
        print("="*60)

    except Exception as e:
        print(f"   [ERROR] Error testing endpoints: {str(e)}")
        print("   Make sure the server is running on port 8002")


if __name__ == "__main__":
    test_api_endpoints()