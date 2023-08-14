import json
import requests
from jwt import decode
from jwt.exceptions import InvalidTokenError

# OktaのIssuer URLとJWTトークン
issuer = "https://dev-flnja182l1uk4brj.us.auth0.com"
jwt_token = "your-jwt-token"

# OktaのIssuer URLからJWKsを取得
jwks_url = f"{issuer}/v1/keys"
jwks_response = requests.get(jwks_url)
jwks_data = jwks_response.json()

# JWKsから公開鍵を取得
public_keys = {}
for jwk in jwks_data['keys']:
    public_keys[jwk['kid']] = {
        'kty': jwk['kty'],
        'kid': jwk['kid'],
        'n': jwk['n'],
        'e': jwk['e']
    }

# JWTトークンを検証
try:
    decoded_token = decode(jwt_token, public_keys, algorithms=['RS256'], issuer=issuer)
    print("JWT Token is valid:")
    print(json.dumps(decoded_token, indent=4))
except InvalidTokenError as e:
    print("JWT Token is invalid:", str(e))
