import asyncio
from app.telegram_bot.bot import bot, dp  # Абсолютный импорт

async def main():
    await dp.start_polling(bot)