import requests
import json
from config import TOKEN  # config.py ファイルからトークンをインポート
url = "https://ron-the-rocker.net/ndrr/api/rooms/2/messages"
#url = "http://localhost:7777/rooms/1/messages"
#url = "http://localhost:7777"

headers = {
    "Authorization": f"Bearer {TOKEN}"
} 
response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    formatted_json = json.dumps(data, indent=4, ensure_ascii=False)
    print(formatted_json)
else:
    print("Error:", response.status_code) 
    print("Error:", response.text) 
