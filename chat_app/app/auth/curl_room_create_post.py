import requests
from config import TOKEN  # Import your token from the config.py file

url = "http://localhost:7777/room/create"
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

data = {
    "name": "New Room Name",
    "label": "Description of the new room",
    "max_capacity": 30,
    "over_karma_limit": 5,
    "under_karma_limit": 5,
    "lux": 10
}

response = requests.post(url, json=data, headers=headers)

if response.status_code != 200:
    print("Request failed with status code:", response.status_code)
    print("Error response:", response.text)
else:
    try:
        response_json = response.json()
        print("Response:", response.status_code, response_json)
    except requests.exceptions.JSONDecodeError:
        print("Response does not contain valid JSON data.")
