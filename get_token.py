import requests

url = "http://127.0.0.1:8000/api-token-auth/"  # or wherever your login endpoint is

data = {
    "username": "eisha",  
    "password": "mirha@2410"   
}

response = requests.post(url, data=data)
print(response.status_code)
print(response.json())

if response.status_code == 200:
    print(response.json())
    