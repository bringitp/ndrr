import requests
import json
from config import TOKEN  # config.py ファイルからトークンをインポート
url = "http://localhost:7777/user/profile"
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

print (response.headers)
