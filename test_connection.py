import requests
import sys

try:
    response = requests.get('http://localhost:5000', timeout=10)
    print(f"Status code: {response.status_code}")
    print(f"Content length: {len(response.text)} bytes")
    print(f"First 100 chars: {response.text[:100]}")
    sys.exit(0)
except Exception as e:
    print(f"Error connecting to server: {e}")
    sys.exit(1)