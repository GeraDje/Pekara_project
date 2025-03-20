from fastapi import APIRouter, Depends
from app.auth.authen import hash_password, create_access_token
from app.auth.dao import UserDAO
from app.auth.dependencies import validate_auth_user, get_current_active_auth_user
from app.auth.schemas import UserRegSchema, UserSchema, TokenInfo
from app.exeptions import UserAlreadyExistsException

router_auth = APIRouter(
    prefix='/auth',
    tags=['Аутентификация и Авторизация']
)

@router_auth.post('/register')
async def register_user(user_data:UserRegSchema):
    existing_user = await UserDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = (hash_password(user_data.password))
    await UserDAO.add(name=user_data.name, email=user_data.email, hashed_password=hashed_password)

@router_auth.post("/login", response_model=TokenInfo)
async def auth_user_issue_jwt(
        user: UserSchema = Depends(validate_auth_user),
):
    access_token = create_access_token(user)
    return TokenInfo(
        access_token=access_token,
        token_type="Bearer"
    )


@router_auth.get("/users/me/")
async def auth_user_check_self_info(
    user: UserSchema = Depends(get_current_active_auth_user),
):
    return {
        "sub": user.id,
        "name": user.name,
        "email": user.email,
    }