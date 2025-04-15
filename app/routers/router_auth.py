from fastapi import APIRouter

from app.shemas.schemas import UserRegister

router = APIRouter(tags=["auth"], prefix="/auth")

@router.post("/")
async def register_user(user: UserRegister):
    pass