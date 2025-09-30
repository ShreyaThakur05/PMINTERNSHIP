#!/usr/bin/env python3
"""
Verify deployment on Render
"""

import requests
import json
import time

API_BASE = "https://pminternship.onrender.com/api"

def test_deployment():
    print("🚀 Testing Render Deployment")
    print("=" * 50)
    
    try:
        # Test health endpoint
        print("1. Testing API Health...")
        response = requests.get(f"{API_BASE}/health", timeout=30)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ API is healthy")
            print(f"   Data Status: {health_data.get('data_status', {})}")
        else:
            print(f"❌ API health check failed")
            return False
        
        # Test stats endpoint
        print("\n2. Testing Stats Endpoint...")
        response = requests.get(f"{API_BASE}/stats", timeout=30)
        if response.status_code == 200:
            stats_data = response.json()
            if stats_data.get('success'):
                stats = stats_data['stats']
                print(f"✅ Stats loaded successfully")
                print(f"   Students: {stats['total_students']}")
                print(f"   Internships: {stats['total_internships']}")
            else:
                print(f"❌ Stats error: {stats_data.get('error')}")
        
        # Test data loading if no data
        if health_data.get('data_status', {}).get('students_loaded', 0) == 0:
            print("\n3. Testing Data Loading...")
            response = requests.post(f"{API_BASE}/load-data", timeout=60)
            if response.status_code == 200:
                load_data = response.json()
                if load_data.get('success'):
                    print(f"✅ Data loaded successfully")
                    print(f"   Message: {load_data.get('message')}")
                else:
                    print(f"❌ Data loading failed: {load_data.get('error')}")
            else:
                print(f"❌ Data loading request failed: {response.status_code}")
        
        print("\n✅ Deployment verification completed!")
        return True
        
    except requests.exceptions.Timeout:
        print("❌ Request timeout - server may be starting up")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - server may be down")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    test_deployment()