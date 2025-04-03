from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from keycloak import KeycloakOpenID
from app.config  import settings


"""
KEYCLOAK_URL=http://localhost:8080
KEYCLOAK_REALM=fastapi-realm
KEYCLOAK_CLIENT_ID=fastapi_app
KEYCLOAK_CLIENT_SECRET=CWvQf0k4lXMEDBvq1T7WHZSLufghWLLP
KEYCLOAK_ADMIN_USERNAME=admin
KEYCLOAK_ADMIN_PASSWORD=admin
CALLBACK_URI=http://localhost:8000/callback
"""
keycloak_openid = KeycloakOpenID(
    server_url=settings.KEYCLOAK_URL,
    client_id=settings.KEYCLOAK_CLIENT_ID,
    realm_name=settings.KEYCLOAK_REALM,
    client_secret_key=settings.KEYCLOAK_CLIENT_SECRET,
    verify=True
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/token"
)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        return keycloak_openid.userinfo(token)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials!",
            headers={"WWW-Authenticate": "Bearer"},
        )

