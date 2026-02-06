import urllib.request
import json
import urllib.error

url = "http://localhost:8000/auth/register"
data = {
    "email": "test_urllib@example.com",
    "password": "password123",
    "role": "candidate",
    "full_name": "Test Candidate"
}
json_data = json.dumps(data).encode('utf-8')

req = urllib.request.Request(url, data=json_data, headers={'Content-Type': 'application/json'})

try:
    print(f"Sending POST request to {url}...")
    with urllib.request.urlopen(req) as response:
        print(f"Status Code: {response.getcode()}")
        print(f"Response: {response.read().decode('utf-8')}")
except urllib.error.HTTPError as e:
    print(f"HTTP Error: {e.code}")
    print(f"Error Response: {e.read().decode('utf-8')}")
except Exception as e:
    print(f"Request failed: {e}")
