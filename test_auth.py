"""Quick test script for authentication"""
import requests
import json

BASE_URL = "http://localhost:5000/api/v1/auth"

def test_register():
    print("\n=== Testing Registration ===")
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "Test1234",
        "full_name": "Test User"
    }
    response = requests.post(f"{BASE_URL}/register", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json()

def test_login():
    print("\n=== Testing Login ===")
    data = {
        "username": "testuser",
        "password": "Test1234"
    }
    response = requests.post(f"{BASE_URL}/login", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json()

if __name__ == "__main__":
    print("Starting authentication tests...")
    print("Make sure the server is running on http://localhost:5000")
    
    try:
        # Test registration
        reg_result = test_register()
        
        # Test login
        login_result = test_login()
        
        print("\n✅ All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to server. Make sure it's running!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
