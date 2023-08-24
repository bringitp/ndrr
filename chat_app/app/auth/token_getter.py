import requests
import jwt
import os

# 例: PATH環境変数を取得
client_secret = os.environ.get('client_secret')

print (client_secret)
keycloak_base_url = "https://ron-the-rocker.net/auth"
realm = "ndrr"
client_id = "python-client"
username = "test1"
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

# KeycloakのURLとRealm名を設定
keycloak_url = "https://ron-the-rocker.net/auth"
realm = "ndrr"  # ご自身のRealm名に置き換えてください

# Keycloakの公開鍵を取得
jwks_url = f"{keycloak_url}/realms/{realm}/protocol/openid-connect/certs"
print (jwks_url)
response = requests.get(jwks_url)
jwks_data = response.json()
public_key = jwt.algorithms.RSAAlgorithm.from_jwk(jwks_data['keys'][0])
options = {"verify_signature": True, "verify_aud": False, "exp": True}

# JWTトークンのデコード
decoded_token = jwt.decode(access_token, public_key, algorithms=["RS256"], options=options)
print(decoded_token)
