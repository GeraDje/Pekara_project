from jwt.exceptions import InvalidTokenError
from fastapi import Form, HTTPException
from fastapi.params import Depends
from starlette import status
from app.auth.authen import validate_password, decode_jwt
from app.auth.dao import UserDAO
from app.auth.schemas import UserSchema
from app.exeptions import Noactive
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials

http_bearer = HTTPBearer()
# oauth2_scheme = OAuth2PasswordBearer(
#     tokenUrl="/auth/login/",
# )

async def validate_auth_user(
        email:str = Form(),
        password:str = Form()
):
    user = await UserDAO.find_one_or_none(email=email)
    if user and validate_password(password, user.hashed_password):
        return user
    raise Noactive


async def get_current_token_payload_user(
        credentials:HTTPAuthorizationCredentials = Depends(http_bearer)
        # token: str = Depends(oauth2_scheme)
)-> dict:
    token = credentials.credentials
    try:
        payload = decode_jwt(
            token=token
    )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"невалидный токен: {e}"
        )
    return payload

async def get_current_auth_user(
        payload:dict = Depends(get_current_token_payload_user,
)):
    email: str = payload.get('email')
    if user := await UserDAO.find_one_or_none(email=email):
        return user
    raise Noactive


def get_current_active_auth_user(
        user:UserSchema = Depends(get_current_auth_user)
):
    return user



