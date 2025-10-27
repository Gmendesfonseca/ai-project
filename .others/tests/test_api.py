#!/usr/bin/env python3
"""
Test script for Task Scheduling API endpoints
"""
import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_task_scheduling_endpoints():
    """Test all task scheduling endpoints"""
    
    # Test data - 4 task problem
    test_data = {
        "tasks": [1, 2, 3, 4],
        "setup_matrix": {
            "(0,1)": 10,
            "(0,2)": 15,
            "(0,3)": 20,
            "(0,4)": 25,
            "(1,2)": 5,
            "(1,3)": 10,
            "(1,4)": 15,
            "(2,1)": 8,
            "(2,3)": 6,
            "(2,4)": 12,
            "(3,1)": 12,
            "(3,2)": 7,
            "(3,4)": 4,
            "(4,1)": 18,
            "(4,2)": 14,
            "(4,3)": 6
        },
        "heuristic": "h1"
    }
    
    print("Testing Task Scheduling API Endpoints")
    print("=" * 50)
    
    # Test A* endpoint
    print("\n1. Testing A* Task Scheduling:")
    try:
        response = requests.post(f"{BASE_URL}/scheduling/task-sequence/a_star", 
                               json=test_data, 
                               headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✓ A* Sequence: {result['sequence']}")
            print(f"   ✓ A* Cost: {result['total_cost']}")
            print(f"   ✓ Algorithm: {result['algorithm']}")
            print(f"   ✓ Setup Details: {len(result['setup_details'])} transitions")
        else:
            print(f"   ✗ A* failed with status: {response.status_code}")
            print(f"   ✗ Error: {response.text}")
    except Exception as e:
        print(f"   ✗ A* request failed: {e}")
    
    # Test Greedy endpoint
    print("\n2. Testing Greedy Task Scheduling:")
    try:
        response = requests.post(f"{BASE_URL}/scheduling/task-sequence/greedy", 
                               json=test_data, 
                               headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✓ Greedy Sequence: {result['sequence']}")
            print(f"   ✓ Greedy Cost: {result['total_cost']}")
            print(f"   ✓ Algorithm: {result['algorithm']}")
        else:
            print(f"   ✗ Greedy failed with status: {response.status_code}")
            print(f"   ✗ Error: {response.text}")
    except Exception as e:
        print(f"   ✗ Greedy request failed: {e}")
    
    # Test Uniform Cost endpoint
    print("\n3. Testing Uniform Cost Task Scheduling:")
    try:
        # Remove heuristic for uniform cost
        uc_data = {
            "tasks": test_data["tasks"],
            "setup_matrix": test_data["setup_matrix"]
        }
        
        response = requests.post(f"{BASE_URL}/scheduling/task-sequence/uniform_cost", 
                               json=uc_data, 
                               headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✓ UC Sequence: {result['sequence']}")
            print(f"   ✓ UC Cost: {result['total_cost']}")
            print(f"   ✓ Algorithm: {result['algorithm']}")
        else:
            print(f"   ✗ Uniform Cost failed with status: {response.status_code}")
            print(f"   ✗ Error: {response.text}")
    except Exception as e:
        print(f"   ✗ Uniform Cost request failed: {e}")
    
    # Test with H2 heuristic
    print("\n4. Testing A* with H2 heuristic:")
    try:
        h2_data = test_data.copy()
        h2_data["heuristic"] = "h2"
        
        response = requests.post(f"{BASE_URL}/scheduling/task-sequence/a_star", 
                               json=h2_data, 
                               headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✓ A*-H2 Sequence: {result['sequence']}")
            print(f"   ✓ A*-H2 Cost: {result['total_cost']}")
            print(f"   ✓ Heuristic: {result['heuristic']}")
        else:
            print(f"   ✗ A*-H2 failed with status: {response.status_code}")
            print(f"   ✗ Error: {response.text}")
    except Exception as e:
        print(f"   ✗ A*-H2 request failed: {e}")
    
    # Test with families (H3 heuristic)
    print("\n5. Testing A* with H3 heuristic (families):")
    try:
        h3_data = test_data.copy()
        h3_data["heuristic"] = "h3"
        h3_data["families"] = {
            1: "A",
            2: "A", 
            3: "B",
            4: "B"
        }
        
        response = requests.post(f"{BASE_URL}/scheduling/task-sequence/a_star", 
                               json=h3_data, 
                               headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✓ A*-H3 Sequence: {result['sequence']}")
            print(f"   ✓ A*-H3 Cost: {result['total_cost']}")
            print(f"   ✓ Heuristic: {result['heuristic']}")
        else:
            print(f"   ✗ A*-H3 failed with status: {response.status_code}")
            print(f"   ✗ Error: {response.text}")
    except Exception as e:
        print(f"   ✗ A*-H3 request failed: {e}")

def test_health_check():
    """Test basic health check endpoint"""
    print("\n6. Testing Health Check:")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("   ✓ Health check passed")
        else:
            print(f"   ✗ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"   ✗ Health check failed: {e}")

if __name__ == "__main__":
    print("Make sure Flask server is running on localhost:5000")
    print("Start it with: source venv/bin/activate && python -m flask run")
    
    # Wait a moment for user to start server
    input("\nPress Enter when server is running...")
    
    test_health_check()
    test_task_scheduling_endpoints()
    
    print("\n" + "=" * 50)
    print("API Testing Complete!")