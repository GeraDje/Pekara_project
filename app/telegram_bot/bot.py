import logging
from aiogram import Bot, Dispatcher
from app.config import settings

logging.basicConfig(level=logging.INFO)
bot = Bot(token=settings.bot_token)
dp = Dispatcher()