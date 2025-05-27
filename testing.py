import requests
import json

# 🔑 Replace with your actual Gemini API key
API_KEY = "AIzaSyBtvAp7zzsKXDwZKgzB4HyXii4qYTBJGXc"

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

headers = {
    "Content-Type": "application/json"
}

data = {
    "contents": [
        {
            "parts": [
                {
                    "text": "Explain how AI works in a few words"
                }
            ]
        }
    ]
}

response = requests.post(url, headers=headers, data=json.dumps(data))

if response.status_code == 200:
    print("✅ Response JSON:")
    print(json.dumps(response.json(), indent=2))
else:
    print(f"❌ Error {response.status_code}: {response.text}")
