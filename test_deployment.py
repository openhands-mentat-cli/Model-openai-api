#!/usr/bin/env python3
"""
Simple test script to validate the deployment works correctly
"""

import requests
import json
import time
import sys

def test_health_endpoint(base_url):
    """Test the health endpoint"""
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health endpoint working")
            return True
        else:
            print(f"❌ Health endpoint returned {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health endpoint failed: {e}")
        return False

def test_models_endpoint(base_url):
    """Test the models endpoint"""
    try:
        response = requests.get(
            f"{base_url}/v1/models",
            headers={"Authorization": "Bearer $$Hello1$$"},
            timeout=10
        )
        if response.status_code == 200:
            models = response.json()
            print(f"✅ Models endpoint working - {len(models.get('data', []))} models available")
            return True
        else:
            print(f"❌ Models endpoint returned {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Models endpoint failed: {e}")
        return False

def test_chat_endpoint(base_url):
    """Test the chat completions endpoint"""
    try:
        response = requests.post(
            f"{base_url}/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer $$Hello1$$"
            },
            json={
                "model": "phi-3-mini-128k",
                "messages": [
                    {"role": "user", "content": "Say 'Hello World' and nothing else."}
                ],
                "max_tokens": 10,
                "temperature": 0.1
            },
            timeout=30
        )
        if response.status_code == 200:
            result = response.json()
            content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            print(f"✅ Chat endpoint working - Response: '{content.strip()}'")
            return True
        else:
            print(f"❌ Chat endpoint returned {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Chat endpoint failed: {e}")
        return False

def main():
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    
    print(f"🧪 Testing deployment at: {base_url}")
    print("=" * 50)
    
    # Wait for server to be ready
    print("⏳ Waiting for server to be ready...")
    for i in range(30):  # Wait up to 30 seconds
        if test_health_endpoint(base_url):
            break
        time.sleep(1)
        if i == 29:
            print("❌ Server did not become ready in time")
            sys.exit(1)
    
    # Run tests
    tests_passed = 0
    total_tests = 3
    
    if test_health_endpoint(base_url):
        tests_passed += 1
    
    if test_models_endpoint(base_url):
        tests_passed += 1
    
    if test_chat_endpoint(base_url):
        tests_passed += 1
    
    print("=" * 50)
    print(f"📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Deployment is working correctly.")
        sys.exit(0)
    else:
        print("❌ Some tests failed. Check the deployment.")
        sys.exit(1)

if __name__ == "__main__":
    main()
