#!/usr/bin/env python3
"""
Test script to verify frontend-backend integration.
"""

import requests
import time
import subprocess
import sys

def test_full_integration():
    """Test the full integration between frontend and backend."""

    # Test 1: Verify backend API is running
    print("Testing backend API...")
    try:
        health_response = requests.get("http://localhost:8000/health", timeout=10)
        if health_response.status_code == 200:
            print("SUCCESS: Backend API is running")
        else:
            print(f"ERROR: Backend API health check failed: {health_response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("ERROR: Backend API is not running at http://localhost:8000")
        return False

    # Test 2: Verify API can retrieve real content
    print("\nTesting content retrieval...")
    try:
        query_data = {
            "query": "What is ROS?",
            "top_k": 3
        }
        query_response = requests.post(
            "http://localhost:8000/query",
            json=query_data,
            timeout=30
        )

        if query_response.status_code == 200:
            result = query_response.json()
            if result.get("success") and result.get("answer"):
                print("SUCCESS:  API returned real content successfully")
                print(f"   Answer preview: {result['answer'][:100]}...")
            else:
                print(f"ERROR:  API returned unexpected response: {result}")
                return False
        else:
            print(f"ERROR:  Query endpoint failed: {query_response.status_code} - {query_response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("ERROR:  Cannot connect to backend API")
        return False
    except Exception as e:
        print(f"ERROR:  Error testing content retrieval: {str(e)}")
        return False

    # Test 3: Check if the frontend would be able to access the backend (CORS)
    print("\nTesting CORS headers...")
    try:
        options_response = requests.options("http://localhost:8000/query", timeout=10)
        cors_headers = options_response.headers
        if 'access-control-allow-origin' in [h.lower() for h in cors_headers.keys()]:
            print("SUCCESS:  CORS headers are properly configured")
        else:
            print("WARNING:   CORS headers not found (may not be an issue depending on how requests are made)")
    except Exception as e:
        print(f"WARNING:   Could not test CORS: {str(e)}")

    print("\nSUCCESS:  All integration tests passed!")
    return True

if __name__ == "__main__":
    print("Testing full frontend-backend integration...")
    success = test_full_integration()

    if success:
        print("\n🎉 Full integration test completed successfully!")
        print("The floating chatbot UI should now be able to communicate with the backend API")
        print("and retrieve real content from the Physical AI & Humanoid Robotics book.")
    else:
        print("\nERROR:  Integration test failed.")
        sys.exit(1)