import httpx
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Dict, Any

# Configuration variables
KEYCLOAK_ISSUER = "https://your-keycloak-server/auth/realms/your-realm"  # Replace with your actual issuer URL
JWKS_URL = f"{KEYCLOAK_ISSUER}/protocol/openid-connect/certs"
ALGORITHMS = ["RS256"]

# Function to fetch Keycloak JWKS
async def fetch_keycloak_jwks() -> Dict[str, Any]:
    async with httpx.AsyncClient() as client:
        response = await client.get(JWKS_URL)
        response.raise_for_status()
        return response.json()

# Function to get the public key from the JWKS
def get_public_key(jwks: Dict[str, Any], kid: str) -> str:
    for key in jwks.get("keys", []):
        if key.get("kid") == kid:
            return jwt.algorithms.RSAAlgorithm.from_jwk(key)
    raise HTTPException(status_code=401, detail="Public key not found")

# Dependency to authenticate using Keycloak JWT
async def keycloak_authenticate(request: Request, auth: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    token = auth.credentials

    try:
        # Fetch the JWKS from Keycloak
        jwks = await fetch_keycloak_jwks()

        # Decode the token header to get the key ID (kid)
        header = jwt.get_unverified_header(token)
        kid = header.get("kid")

        if not kid:
            raise HTTPException(status_code=401, detail="Token does not contain key ID")

        # Get the public key corresponding to the key ID
        public_key = get_public_key(jwks, kid)

        # Decode and validate the JWT token
        payload = jwt.decode(token, public_key, algorithms=ALGORITHMS, audience=KEYCLOAK_ISSUER)
        request.state.user = payload  # Store the user info in the request state

    except JWTError as e:
        raise HTTPException(status_code=401, detail="Token is invalid or expired") from e
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=502, detail="Failed to fetch Keycloak public key") from e

    return payload