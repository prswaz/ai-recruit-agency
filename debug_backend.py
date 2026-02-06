import requests
import sys

BASE_URL = "http://localhost:8000"

def test_backend():
    print(f"Testing connectivity to {BASE_URL}...")
    try:
        r = requests.get(f"{BASE_URL}/")
        print(f"Root: {r.status_code} {r.json()}")
    except Exception as e:
        print(f"Failed to connect to root: {e}")
        return

    # 1. Login to get token (using a known user or registering one)
    email = "test_candidate@example.com"
    password = "password123"
    
    print(f"\nAttempting to register/login {email}...")
    
    # Try register first just in case
    try:
        reg_payload = {"email": email, "password": password, "role": "candidate", "full_name": "Test Candidate"}
        r = requests.post(f"{BASE_URL}/auth/register", json=reg_payload)
        print(f"Register: {r.status_code}")
    except Exception as e:
        print(f"Register failed (might exist): {e}")

    # Login
    try:
        data = {"username": email, "password": password}
        r = requests.post(f"{BASE_URL}/auth/token", data=data)
        if r.status_code != 200:
            print(f"Login failed: {r.status_code} {r.text}")
            return
        
        token = r.json()["access_token"]
        print(f"Login successful. Token obtained.")
        
        headers = {"Authorization": f"Bearer {token}"}
        
        # 2. Get Profile
        print("\nFetching /candidates/me ...")
        r = requests.get(f"{BASE_URL}/candidates/me", headers=headers, timeout=5)
        print(f"Profile Status: {r.status_code}")
        print(f"Profile Data: {r.text[:200]}...") # Print first 200 chars
        
        if r.status_code == 200:
            print("SUCCESS: Profile endpoint is working.")
        else:
            print("FAILURE: Profile endpoint returned error.")
            
    except Exception as e:
        print(f"Login/Fetch failed: {e}")

if __name__ == "__main__":
    test_backend()
