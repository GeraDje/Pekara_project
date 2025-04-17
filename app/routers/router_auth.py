from fastapi import APIRouter,HTTPException,status
from app.authenticator.crud import get_password_hash
from app.authenticator.keycloak_auth import register_user
from app.dao.usersdao import UserDAO
from app.exeptions import UserAlreadyExistsException
from app.schemas.user import UserCreate

router = APIRouter(tags=["auth"], prefix="/auth")

@router.post('/register')
async def register(user_data: UserCreate):
    existing_user = await UserDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    try:
        # Регистрация пользователя в Keycloak
        user = await register_user(user_data)
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {str(e)}"
        )
    else:
        hashed_password = get_password_hash(user_data.password)
        await UserDAO.add(name=user_data.name, email=user_data.email, hashed_password=hashed_password, role_id=2)


