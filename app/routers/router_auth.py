from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from keycloak import KeycloakOpenID, KeycloakAdmin

from app.authenticator.crud import get_user_by_email, create_user
from app.config import settings
from app.exeptions import UserAlreadyExistsException
from app.shemas.schemas import UserCreate

router = APIRouter( tags=["Авторизация и аунтификация"])

keycloak_openid = KeycloakOpenID(server_url=settings.KEYCLOAK_URL,
                                  client_id=settings.KEYCLOAK_CLIENT_ID,
                                  realm_name=settings.KEYCLOAK_REALM)

keycloak_admin = KeycloakAdmin(server_url=settings.KEYCLOAK_URL,
                                username=settings.KEYCLOAK_ADMIN_USERNAME,
                                password=settings.KEYCLOAK_ADMIN_PASSWORD,
                                realm_name=settings.KEYCLOAK_REALM,
                                client_id=settings.KEYCLOAK_CLIENT_ID,
                                verify=True)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/registration", )
async def registracia(user_data:UserCreate):
    try:
        new_user = await get_user_by_email(user_data.email)
        if new_user:
            raise UserAlreadyExistsException
        else:
            try:
                keycloak_admin.create_user({
                    "username": user_data.name,
                    "email": user_data.email,
                    "enabled": True,
                    "credentials": [{
                        "type": "password",
                        "value": user_data.password,
                        "temporary": False  # Устанавливаем временный пароль в False
                    }]
                })
            except Exception as e:
                print(f"Ошибка при подключении к Keycloak: {e}")
            await create_user(user_data)
            return {"msg": "User registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/token", )
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        token = keycloak_openid.token(form_data.username, form_data.password)
        return token
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/user/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    try:
        userinfo = keycloak_openid.userinfo(token)
        return userinfo
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))