import requests
from config import TOKEN  # config.py ファイルからトークンをインポート

url = "http://localhost:7777/room/1/change_owner"
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

data = {
    "new_owner_id": 2  # ここに追加するユーザーのIDを指定
}

response = requests.put(url, json=data, headers=headers)

if response.status_code != 200:
    print("Request failed with status code:", response.status_code)
    print("Error response:", response.text)
else:
    try:
        response_json = response.json()
        print("Response:", response.status_code, response_json)
    except requests.exceptions.JSONDecodeError:
        print("Response does not contain valid JSON data.")
