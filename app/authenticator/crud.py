from passlib.context import CryptContext
from app.dao.usersdao import UserDAO
from app.shemas.schemas import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_user( user_id: int):
    user = await UserDAO.find_one_or_none(id=user_id)
    if user is None:
        raise Exception("User not found")
    return user

async def get_user_by_email(email: str):
    user = await UserDAO.find_one_or_none(email=email)
    return user

async def create_user(user:UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = await UserDAO.add(
        email=user.email,
        name=user.name,
        hashed_password=hashed_password,
        role_id=2  # По умолчанию роль продавца
    )
    return db_user

def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)