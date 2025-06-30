import requests
import json

# Test the AI caption generation endpoint
url = "http://localhost:8000/ai/generate-caption"

# Test data (this will be sent from the Flutter app)
test_data = {
    "product_name": "Handmade Silver Ring",
    "price": "1500",
    "description": "Beautiful silver ring with intricate patterns",
    "category": "jewelry"
}

try:
    response = requests.post(url, json=test_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")
