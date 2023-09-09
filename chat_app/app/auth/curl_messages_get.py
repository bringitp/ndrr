import requests
import json
from config import TOKEN  # config.py ファイルからトークンをインポート

url = "https://ron-the-rocker.net/ndrr/api/room/1/messages"
#url = "http://localhost:7777/room/1/messages"
#url = "http://localhost:7777"

previous_etag = "1a5d5db37a4ef9d2312b1646bfe024609"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "If-None-Match": f"{previous_etag}"
} 

response = requests.get(url, headers=headers)

if response.status_code == 200:
    # Check if the "ETag" header is present in the response
    if 'etag' in response.headers:
        etag = response.headers['ETag']
        print(f"ETag found: {etag}")
    else:
        print("ETag not found in the response headers.")
    
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

print (response.headers)
