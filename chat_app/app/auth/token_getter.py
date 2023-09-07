import requests
import jwt
import os

# 環境変数からクライアントシークレットを取得
client_secret = os.environ.get('client_secret')
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

#response = requests.post(token_url, data=payload)

#if response.status_code == 200:
#    token_data = response.json()
#    access_token = token_data.get("access_token")
#    print("Access Token:", access_token)
#else:
#    print("Failed to retrieve access token. Status code:", response.status_code)
#    print("Response:", response.text)

# KeycloakのURLとRealm名を設定

access_token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJiaXJGWk42NldMakpZYlhIb1VvZVYzX1l6amlhbVJ4QWZEbWxTRWxEQlBJIn0.eyJleHAiOjE2OTQyMDIxOTgsImlhdCI6MTY5NDA5NDE5OCwianRpIjoiZTFmNjNjOTktOGI2Zi00MGRmLWIwZGEtMDU3NjI4ZTRjYWE1IiwiaXNzIjoiaHR0cHM6Ly9yb24tdGhlLXJvY2tlci5uZXQvYXV0aC9yZWFsbXMvbmRyciIsInN1YiI6IjMxNTFmY2ZhLTAxNTYtNGI4OS1iZjMxLWNlYzNkMDliYWExMSIsInR5cCI6IkJlYXJlciIsImF6cCI6InB5dGhvbi1jbGllbnQiLCJzZXNzaW9uX3N0YXRlIjoiMTg2ZTQwYTQtNWUzNC00YmI3LTk1OGQtMzczODhhYTBmOGZjIiwic2NvcGUiOiIiLCJzaWQiOiIxODZlNDBhNC01ZTM0LTRiYjctOTU4ZC0zNzM4OGFhMGY4ZmMifQ.Eax_TzPsqJ9Desa6gdfEymfpBdqPG-5a8sOkK9eW1Y7gF6JAqU5cWJ-sG9MUMHxdaQMXbWZ3rO3sL9BxP7jO7ZE1Wi3OGKojsap9OrbfStMp-V5LgeTfi5Yu31v_jmKzf-yWc2snsDpKTNq020UZynz2auyp9Et5wtOhyfITzF7hw831G9DmQzxZWSTDOEjRQUBHBUM87MwA_a4WIIZdiRwF77hhTPPHUQe-E-FE3ubZTfKlOgJHMEAoSxdmoVdd0bW2bjhCwARH1acsrxT0xwh2_NfRzTg0ddvJoMgq6-tiyusfeEujiw5BqlQYn7ofKnRXK9nctNJdxsZJ7FJ7vA"




keycloak_url = "https://ron-the-rocker.net/auth"
realm = "ndrr"  # ご自身のRealm名に置き換えてください

# Keycloakの公開鍵を取得とキャッシュ
jwks_url = f"{keycloak_url}/realms/{realm}/protocol/openid-connect/certs"
response = requests.get(jwks_url)
jwks_data = response.json()
public_key = jwt.algorithms.RSAAlgorithm.from_jwk(jwks_data['keys'][0])

# JWTトークンのデコード
decoded_token = jwt.decode(access_token, public_key, algorithms=["RS256"])
print(decoded_token)
