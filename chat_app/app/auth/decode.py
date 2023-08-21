import jwt
import requests

jwt_token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJhemxKdHZFUUFQR09FTVlnWDhUd1FTYWt3ZHZveUIzZVRSTGRTMUd0dWFvIn0.eyJleHAiOjE2OTI1ODEyNzEsImlhdCI6MTY5MjU4MDk3MSwianRpIjoiZDM3ZDA0N2YtMTM0My00YWMzLWI3OTAtMzU1ZWVhYWI0Zjg2IiwiaXNzIjoiaHR0cHM6Ly9yb24tdGhlLXJvY2tlci5uZXQvYXV0aC9yZWFsbXMvbmRyciIsInN1YiI6IjJhY2E5NTZhLWM0ZjAtNGFmNy1iNzhmLWFiMzNlN2E2ZWExMyIsInR5cCI6IkJlYXJlciIsImF6cCI6InB5dGhvbi1jbGllbnQiLCJzZXNzaW9uX3N0YXRlIjoiZTU1MmU0ZTMtNzMzNy00ZDE3LWI1ZmMtN2E3ZTcxMWQwMzk4Iiwic2NvcGUiOiIiLCJzaWQiOiJlNTUyZTRlMy03MzM3LTRkMTctYjVmYy03YTdlNzExZDAzOTgifQ.U463OGA6LI6K1FKFsLOvFD0mqYdrF9O5cZJqASUYboYvWhgJ7rWM-sCDOW4ormnMYr2VRcJu4jXoL8XZXkSg0_EjdLdCRmQl8hBcIqbeUA1fpHReVFJzPT9Vn3Gk9epgnYVnRzk_ODmoBfCUmI2XniVJ2groS7JnkpQHRm1RwCxqWfHguK8SVMqkMZu9X7jX-hhYcrgyGPH6htOIWnSQMLu6sEIueykhhlInMbEsnCgOt7jr01v6-K5oXAYZZLwr6W0HNALu7wX5A_FpGfKWDNw9Fb7S1o37-E-U8UVV0C0i-rsCB-NFfYON6IgLwgOhGyu1sBrCEKL3efzONwRtBg"
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
decoded_token = jwt.decode(jwt_token, public_key, algorithms=["RS256"], options=options)
print(decoded_token)