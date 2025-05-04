import requests

url = "http://127.0.0.1:8000/api/rides/"
headers = {
    "Authorization": "Token 09f2c13794a5741beccdae3a3b0f8f021ecd5888" 
}
data = {
    "origin": "Lahore, Pakistan",
    "destination": "Islamabad, Pakistan",
    "date": "2025-05-04",
    "time": "15:30:00",
    "seats_available": 3
}

response = requests.post(url, json=data, headers=headers)
print(response.status_code)
try:
    print(response.json())
except Exception:
    print("Response Text:", response.text)