from app.dao.usersdao import UserDAO
from functools import wraps
from aiogram import types



def access_required(func):
    @wraps(func)
    async def wrapper(message: types.Message, *args, **kwargs):
        if not await UserDAO.find_one_or_none(email=str(message.from_user.id)):
            await message.answer("🚫 Доступ запрещен")
            return
        return await func(message, *args, **kwargs)
    return wrapper