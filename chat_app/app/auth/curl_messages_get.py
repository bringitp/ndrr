import requests
import json
from config import TOKEN  # config.py ファイルからトークンをインポート

url = "https://ron-the-rocker.net/ndrr/api/room/1/messages"
#url = "http://localhost:7777/room/1/messages"
#url = "http://localhost:7777"SQL
headers = {
    "Authorization": f"Bearer {TOKEN}"
} 

response = requests.get(url, headers=headers)

if response.status_code == 200:
    # Check if the response has a Content-Encoding header and if it's set to "gzip"
    if 'Content-Encoding' in response.headers and response.headers['Content-Encoding'] == 'gzip':
        print("Response is Gzipped.")
    else:
        print("Response is not Gzipped.")
    
    data = response.json()
    formatted_json = json.dumps(data, indent=4, ensure_ascii=False) 
    print(formatted_json)
else:
    print("Error:", response.status_code) 
    print("Error:", response.text) 