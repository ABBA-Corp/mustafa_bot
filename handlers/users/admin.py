from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from keyboards.inline.admin_keys import *
from keyboards.inline.menu_button import *
from utils.db_api import database as commands
from loader import dp, bot
from utils.db_api.database import *
from aiogram.dispatcher.filters.builtin import Command
from data import config


@dp.message_handler(lambda message: message.text in ["/admin"], state='*')
async def admin_menu(message: types.Message, state: FSMContext):
    keyboard = await admin_category_keyboard()
    await message.answer(text="Kerakli kategoriyani tanlang 👇", reply_markup=keyboard)
    await state.set_state("admin_category")


@dp.callback_query_handler(state='admin_category')
async def get_product_admin(call: types.CallbackQuery, state: FSMContext):
    data = call.data
    if data == "back":
        await call.message.delete()
        lang = await get_lang(call.from_user.id)
        markup = await user_menu(lang)
        markup = await user_menu(lang)
        if lang == "uz":
            await bot.send_message(chat_id=call.from_user.id, text="Botimizga xush kelibsiz. Iltimos kerakli bo'limni tanlang 👇", reply_markup=markup)
        elif lang == "tr":
            await bot.send_message(chat_id=call.from_user.id, text="Botumuza hoş geldiniz. İstediğiniz bölümü seçin👇", reply_markup=markup)
        elif lang == "ru":
            await bot.send_message(chat_id=call.from_user.id, text="Добро пожаловать в наш бот. Пожалуйста, выберите нужный раздел 👇", reply_markup=markup)
        await state.set_state("get_command")
    else:
        keyboard = await admin_product_keyboard(data)
        await call.message.edit_text(text="Выберите продукт для добавления в STOP_LIST 👇", reply_markup=keyboard)
        await state.set_state("admin_product")


@dp.callback_query_handler(state='admin_product')
async def get_product_admin(call: types.CallbackQuery, state: FSMContext):
    data = call.data
    if data == "back":
        keyboard = await admin_category_keyboard()
        await call.message.edit_text(text="Выберите нужную категорию 👇", reply_markup=keyboard)
        await state.set_state("admin_category")
    else:
        product = await get_product(data)
        if product.stop_list:
            product.stop_list = False
        else:
            product.stop_list = True
        product.save()
        keyboard = await admin_product_keyboard(product.category.id)
        await call.message.edit_text(text="Выберите продукт для добавления в STOP_LIST 👇", reply_markup=keyboard)
        await state.set_state("admin_product")
