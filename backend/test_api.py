#!/usr/bin/env python3
"""
Simple test script to verify the API server is working correctly.
"""

import requests
import json

def test_api_health():
    """Test the health endpoint of the API."""
    try:
        # Test health endpoint
        response = requests.get("http://localhost:8000/health", timeout=10)
        print(f"Health check status: {response.status_code}")
        if response.status_code == 200:
            print("[SUCCESS] API server is healthy")
            return True
        else:
            print(f"[ERROR] API server health check failed: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("[ERROR] API server is not running at http://localhost:8000")
        return False
    except Exception as e:
        print(f"[ERROR] Error checking API health: {str(e)}")
        return False

def test_query_endpoint():
    """Test the query endpoint with a simple query."""
    try:
        # Test query endpoint
        query_data = {
            "query": "What is Physical AI?",
            "top_k": 3
        }
        response = requests.post(
            "http://localhost:8000/query",
            json=query_data,
            timeout=30
        )
        print(f"Query endpoint status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("[SUCCESS] Query endpoint working")
            print(f"Response keys: {list(result.keys())}")
            return True
        else:
            print(f"[ERROR] Query endpoint failed: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("[ERROR] API server is not running at http://localhost:8000")
        return False
    except Exception as e:
        print(f"[ERROR] Error testing query endpoint: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing API server endpoints...")

    print("\n1. Testing health endpoint...")
    health_ok = test_api_health()

    print("\n2. Testing query endpoint...")
    query_ok = test_query_endpoint()

    print(f"\nResults:")
    print(f"- Health check: {'[SUCCESS]' if health_ok else '[ERROR]'}")
    print(f"- Query endpoint: {'[SUCCESS]' if query_ok else '[ERROR]'}")

    if health_ok and query_ok:
        print("\n[SUCCESS] API server is working correctly!")
    else:
        print("\n[ERROR] API server issues detected.")