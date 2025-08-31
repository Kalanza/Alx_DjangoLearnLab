"""
Test script for Social Media API endpoints.
This script demonstrates how to interact with the API programmatically.
"""

import requests
import json

# Base URL for the API
BASE_URL = "http://127.0.0.1:8000/api"

def test_user_registration():
    """Test user registration endpoint."""
    print("Testing user registration...")
    
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123",
        "password_confirm": "testpassword123",
        "first_name": "Test",
        "last_name": "User",
        "bio": "This is a test user account"
    }
    
    response = requests.post(f"{BASE_URL}/register/", json=user_data)
    
    if response.status_code == 201:
        print("✅ User registration successful!")
        data = response.json()
        print(f"Username: {data['user']['username']}")
        print(f"Token: {data['token']}")
        return data['token']
    else:
        print("❌ User registration failed!")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def test_user_login():
    """Test user login endpoint."""
    print("\nTesting user login...")
    
    login_data = {
        "username": "testuser",
        "password": "testpassword123"
    }
    
    response = requests.post(f"{BASE_URL}/login/", json=login_data)
    
    if response.status_code == 200:
        print("✅ User login successful!")
        data = response.json()
        print(f"Username: {data['user']['username']}")
        print(f"Token: {data['token']}")
        return data['token']
    else:
        print("❌ User login failed!")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def test_profile_access(token):
    """Test profile access with authentication."""
    print("\nTesting profile access...")
    
    headers = {"Authorization": f"Token {token}"}
    response = requests.get(f"{BASE_URL}/profile/", headers=headers)
    
    if response.status_code == 200:
        print("✅ Profile access successful!")
        data = response.json()
        print(f"User ID: {data['id']}")
        print(f"Username: {data['username']}")
        print(f"Email: {data['email']}")
        print(f"Bio: {data['bio']}")
        print(f"Followers: {data['followers_count']}")
        print(f"Following: {data['following_count']}")
    else:
        print("❌ Profile access failed!")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")

def test_profile_update(token):
    """Test profile update functionality."""
    print("\nTesting profile update...")
    
    headers = {"Authorization": f"Token {token}"}
    update_data = {
        "bio": "Updated bio - I'm a test user with new information!",
        "first_name": "Updated",
        "last_name": "TestUser"
    }
    
    response = requests.put(f"{BASE_URL}/profile/", json=update_data, headers=headers)
    
    if response.status_code == 200:
        print("✅ Profile update successful!")
        data = response.json()
        print(f"Updated bio: {data['bio']}")
        print(f"Updated name: {data['first_name']} {data['last_name']}")
    else:
        print("❌ Profile update failed!")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")

def main():
    """Main test function."""
    print("🚀 Starting Social Media API Tests")
    print("=" * 50)
    
    # Test registration
    token = test_user_registration()
    
    if token:
        # Test profile access
        test_profile_access(token)
        
        # Test profile update
        test_profile_update(token)
        
        # Test login (using existing user)
        login_token = test_user_login()
        
        if login_token:
            print(f"\n✅ All tests completed successfully!")
            print(f"Token from registration: {token[:20]}...")
            print(f"Token from login: {login_token[:20]}...")
            print("The tokens should be the same for the same user.")
    
    print("\n" + "=" * 50)
    print("🏁 Test execution completed")

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the API server.")
        print("Make sure the Django development server is running:")
        print("python manage.py runserver")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
