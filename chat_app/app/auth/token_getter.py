import requests
import os

# 例: PATH環境変数を取得
client_secret = os.environ.get('client_secret')

# Keycloakの設定
keycloak_base_url = "https://ron-the-rocker.net/auth"
realm = "ndrr"
client_id = "python-client"
username = "test0"
password = "testtest"

# トークンエンドポイントにリクエストを送信してトークンを取得
token_url = f"{keycloak_base_url}/realms/{realm}/protocol/openid-connect/token"
payload = {
    "grant_type": "password",
    "client_id": client_id,
    "client_secret": client_secret,
    "username": username,
    "password": password
}

response = requests.post(token_url, data=payload)

if response.status_code == 200:
    token_data = response.json()
    access_token = token_data.get("access_token")
    print("Access Token:", access_token)
else:
    print("Failed to retrieve access token. Status code:", response.status_code)
    print("Response:", response.text)