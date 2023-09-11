import requests
from config import TOKEN  # Import your token from the config.py file

# テスト対象の部屋のIDを指定
room_id_to_destroy = 1  # これを削除したい部屋のIDに置き換えてください

# Destroy Room APIのURL
url = f"http://localhost:7777/room/{room_id_to_destroy}/destroy"

# ヘッダーにトークンを設定
headers = {
    "Authorization": f"Bearer {TOKEN}"
}

# Destroyリクエストを送信
response = requests.delete(url, headers=headers)

if response.status_code != 200:
    print("Request failed with status code:", response.status_code)
    print("Error response:", response.text)
else:
    try:
        response_json = response.json()
        print("Response:", response.status_code, response_json)
    except requests.exceptions.JSON
print("Response does not contain valid JSON data.")