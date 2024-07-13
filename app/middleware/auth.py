import requests
from jose import jwt
from jose.exceptions import JWTError
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

KEYCLOAK_URL = "https://<your-keycloak-domain>/auth/realms/<your-realm>"
KEYCLOAK_CLIENT_ID = "<your-client-id>" # get from env
KEYCLOAK_CLIENT_SECRET = "<your-client-secret>" # get from env

def get_keycloak_public_key():
    url = f"{KEYCLOAK_URL}/protocol/openid-connect/certs"
    response = requests.get(url)
    response.raise_for_status()
    jwks = response.json()
    return jwks

def decode_jwt(token):
    try:
        jwks = get_keycloak_public_key()
        # Get the key id from the token headers
        headers = jwt.get_unverified_headers(token)
        kid = headers["kid"]
        
        # Find the key with the matching key id
        key = next(key for key in jwks["keys"] if key["kid"] == kid)
        
        # Prepare the public key
        public_key = jwt.algorithms.RSAAlgorithm.from_jwk(key)
        
        # Decode and verify the token
        decoded_token = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            audience=KEYCLOAK_CLIENT_ID,
            issuer=KEYCLOAK_URL
        )
        return decoded_token
    except JWTError as e:
        print(f"JWT verification failed: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Auth middleware
async def auth_user(token: str = Depends(oauth2_scheme)):
    return decode_jwt(token)