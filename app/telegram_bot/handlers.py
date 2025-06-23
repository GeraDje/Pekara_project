from aiogram import types, F
from aiogram.filters.command import Command
from app.telegram_bot.bot import dp
from app.telegram_bot.auth import access_required
from app.dao.recieptsdao import ReceiptsDAO


@dp.message(Command("start"))
@access_required
async def cmd_start(message: types.Message):
    kb = [
        [types.KeyboardButton(text="За сегодня")],
        [types.KeyboardButton(text="За неделю")],
        [types.KeyboardButton(text="За месяц")]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите период"
    )
    await message.answer("Выберите период:", reply_markup=keyboard)

@dp.message(F.text.lower() == "за сегодня")
@access_required
async def today_report(message: types.Message):
    result = await ReceiptsDAO.get_sum_today()
    await message.reply(f"Сумма за сегодня: {result}")

@dp.message(F.text.lower() == "за неделю")
@access_required
async def week_report(message: types.Message):
    result = await ReceiptsDAO.get_sum_to_week()
    await message.reply(f"Сумма за неделю: {result}")

@dp.message(F.text.lower() == "за месяц")
@access_required
async def mounth_report(message: types.Message):
    result = await ReceiptsDAO.get_sum_mounth()
    await message.reply(f"Сумма за месяц: {result}")