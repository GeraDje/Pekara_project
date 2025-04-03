from fastapi import APIRouter
from app.authenticator.crud import get_user_by_email, create_user
from app.exeptions import UserAlreadyExistsException
from app.shemas.schemas import UserCreate

router = APIRouter(prefix="/auth", tags=["Авторизация и аунтификация"])

@router.post("/registration", )
async def registracia(user_data:UserCreate):
    new_user = await get_user_by_email(user_data.email)
    if new_user:
        raise UserAlreadyExistsException
    await create_user(user_data)

