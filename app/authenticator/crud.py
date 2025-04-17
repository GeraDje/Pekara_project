from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from app.dao.usersdao import UserDAO

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

async def get_user( user_email: str):
    user = await UserDAO.find_one_or_none(email=user_email)
    if user is None:
        raise Exception("User not found")
    return user


