#!/usr/bin/env python3
"""
Simple test script to verify the internship allocation system works
"""

import requests
import json
import time

API_BASE = "http://localhost:5000/api"

def test_api_endpoint(endpoint, method="GET", data=None):
    """Test an API endpoint"""
    try:
        url = f"{API_BASE}{endpoint}"
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        
        print(f"{method} {endpoint}: {response.status_code}")
        result = response.json()
        
        if response.status_code == 200:
            print(f"✅ Success: {result.get('message', 'OK')}")
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")
        
        return result
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return None

def main():
    print("🧪 Testing InternNet System")
    print("=" * 50)
    
    # Test 1: Health check
    print("\n1. Testing API Health...")
    health = test_api_endpoint("/health")
    
    # Test 2: Load data
    print("\n2. Testing Data Loading...")
    load_result = test_api_endpoint("/load-data", "POST")
    
    # Test 3: Get stats
    print("\n3. Testing Stats...")
    stats = test_api_endpoint("/stats")
    if stats and stats.get('success'):
        print(f"   Students: {stats['stats']['total_students']}")
        print(f"   Internships: {stats['stats']['total_internships']}")
        print(f"   Capacity: {stats['stats']['total_capacity']}")
    
    # Test 4: Run allocation
    print("\n4. Testing Allocation...")
    allocation = test_api_endpoint("/allocate", "POST")
    if allocation and allocation.get('success'):
        result = allocation['result']
        print(f"   Allocated: {result['total_allocated']}")
        print(f"   Total Score: {result['total_score']:.2f}")
    
    # Test 5: Test chatbot
    print("\n5. Testing RAG Chatbot...")
    chat_result = test_api_endpoint("/chat", "POST", {
        "question": "How many students were allocated?"
    })
    if chat_result and not chat_result.get('error'):
        print(f"   Response: {chat_result.get('answer', 'No answer')[:100]}...")
    
    print("\n" + "=" * 50)
    print("🎉 System test completed!")

if __name__ == "__main__":
    main()