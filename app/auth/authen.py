from datetime import timedelta, datetime
import jwt
import bcrypt
from app.shemas.schemas import UserSchema
from app.config import settings

def encode_jwt(
    payload: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
) -> str: # кодирование токена
    to_encode = payload.copy()
    now = datetime.utcnow()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now,
    )
    encoded = jwt.encode(to_encode,private_key, algorithm=algorithm)
    return encoded

def decode_jwt(
    token: str | bytes,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
) -> dict:
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return decoded

def hash_password(password:str) -> bytes: # хеширование пароля
    salt = bcrypt.gensalt()
    password_bytes = password.encode()
    return bcrypt.hashpw(password_bytes, salt)

def validate_password(
        password:str,
        hashed_password:bytes,
) -> bool:                       #проверка пароля
    return bcrypt.checkpw(
        password.encode(),
        hashed_password=hashed_password)

TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"

def create_jwt_token(
        token_type:str,
        token_data: dict,
        expire_minutes:int = settings.auth_jwt.access_token_expire_minutes,
        expire_timedelta: timedelta | None = None,
)->str:
    jwt_payload = {
        TOKEN_TYPE_FIELD:token_type,
    }
    jwt_payload.update(token_data)
    token = encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
    )
    return token


def create_access_token( user: UserSchema):
    jwt_payload = {
        "sub": str(user.id),
        "name": user.name,
        "email": user.email,
    }
    token = create_jwt_token(
        token_type=ACCESS_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_minutes=settings.auth_jwt.access_token_expire_minutes,
    )
    return token

def create_refresh_token( user: UserSchema):
    jwt_payload = {
        "sub": str(user.id),
    }
    token = create_jwt_token(
        token_type=REFRESH_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_timedelta=timedelta(days=settings.auth_jwt.refresh_token_expire_days),
    )
    return token