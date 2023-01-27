from loader import dp, bot
from aiogram import types
from aiogram.types import ReplyKeyboardRemove

from utils.db_api.database import get_lang


@dp.message_handler(lambda message: message.text not in ['/admin'], state=None)
async def bot_echo(message: types.Message):
    lang = await get_lang(message.from_id)
    if lang == "uz":
        await message.answer("🤖💬: Botni ishga tushirish uchun  /start buyrug'idan foydalaning", reply_markup=ReplyKeyboardRemove())
    if lang == "en":
        await message.answer("🤖💬: Use the /start command to start the bot", reply_markup=ReplyKeyboardRemove())
    if lang == "ru":
        await message.answer("🤖💬: Используйте команду /start для запуска бота", reply_markup=ReplyKeyboardRemove())
