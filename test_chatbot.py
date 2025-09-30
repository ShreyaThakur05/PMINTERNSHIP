#!/usr/bin/env python3
"""
Simple test script to verify chatbot functionality
"""

import requests
import json

def test_chatbot():
    """Test the chatbot API endpoint"""
    
    # Test API health first
    try:
        health_response = requests.get('http://localhost:5000/api/health')
        print(f"API Health Status: {health_response.status_code}")
        if health_response.status_code == 200:
            print(f"Health Response: {health_response.json()}")
        else:
            print("API is not healthy")
            return
    except Exception as e:
        print(f"Cannot connect to API: {e}")
        return
    
    # Test chatbot endpoint
    test_questions = [
        "Hello",
        "How many students are in the system?",
        "What is the quota for SC category?",
        "Tell me about the allocation system"
    ]
    
    for question in test_questions:
        print(f"\n--- Testing Question: '{question}' ---")
        
        try:
            response = requests.post(
                'http://localhost:5000/api/chat',
                json={'question': question},
                headers={'Content-Type': 'application/json'}
            )
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"Response: {result}")
            else:
                print(f"Error Response: {response.text}")
                
        except Exception as e:
            print(f"Request failed: {e}")

if __name__ == "__main__":
    test_chatbot()