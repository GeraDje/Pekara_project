from keycloak import KeycloakOpenID, KeycloakAdmin
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from app.config import settings
from typing import Dict, Any

from app.schemas.user import UserCreate

# Инициализация Keycloak клиента
keycloak_openid = KeycloakOpenID(
    server_url=settings.KEYCLOAK_URL,
    client_id=settings.KEYCLOAK_CLIENT_ID,
    realm_name=settings.KEYCLOAK_REALM,
    client_secret_key=settings.KEYCLOAK_CLIENT_SECRET,
)

# Инициализация Keycloak Admin клиента
keycloak_admin = KeycloakAdmin(
    server_url=settings.KEYCLOAK_URL,
    username=settings.KEYCLOAK_ADMIN_USER,
    password=settings.KEYCLOAK_ADMIN_PASSWORD,
    realm_name=settings.KEYCLOAK_REALM,
    client_id=settings.KEYCLOAK_CLIENT_ID,
    client_secret_key=settings.KEYCLOAK_CLIENT_SECRET,
    verify=True
)

# Настройка OAuth2 схемы
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/auth",
    tokenUrl=f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/token",
)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        # Получение информации о пользователе из токена
        userinfo = keycloak_openid.userinfo(token)
        return userinfo
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_token(email: str, password: str):
    try:
        # Получение токена с правильными параметрами
        token = keycloak_openid.token(
            username=email,
            password=password,
            grant_type="password",
            client_id=settings.KEYCLOAK_CLIENT_ID,
            client_secret=settings.KEYCLOAK_CLIENT_SECRET
        )
        return token
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )


def refresh_token(refresh_token: str):
    try:
        # Обновление токена с правильными параметрами
        token = keycloak_openid.refresh_token(
            refresh_token=refresh_token,
            client_id=settings.KEYCLOAK_CLIENT_ID,
            client_secret=settings.KEYCLOAK_CLIENT_SECRET
        )
        return token
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )


def register_user(user_data: UserCreate) -> Dict[str, Any]:
    try:
        # Создание пользователя в Keycloak
        new_user = keycloak_admin.create_user({
            "username": user_data.email,
            "email": user_data.email,
            "first_name": user_data.name,
            "enabled": True,
            "credentials": [{
                "type": "password",
                "value": user_data.password,
                "temporary": False
            }]
        })

        # Получение ID созданного пользователя
        user_id = new_user

        # Установка пароля
        keycloak_admin.set_user_password(user_id, user_data.password, temporary=False)

        return {
            "id": user_id,
            "username": user_data.email,
            "email": user_data.email,
            "first_name": user_data.name,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create user: {str(e)}"
        )

