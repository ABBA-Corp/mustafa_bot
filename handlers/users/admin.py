from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from handlers.users.taxi import create_order
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


@dp.callback_query_handler(chat_type=types.ChatType.GROUP, state='*')
async def get_conf(c: types.CallbackQuery, scheduler: AsyncIOScheduler):

    if c.data.startswith('co'):
        order_id = str(c.data).replace("co", "")
        await c.message.edit_text(f"Buyurtma: #{order_id}\n"
                                  f"Qabul qilindi ✅")
        res = await get_order(order_id)
        order_details = await get_order_details(order_id)
        cooking_times = []
        print(res.user.name)
        for order_detail in order_details:
            cooking_times.append(order_detail.product.cooking_time)
        scheduler.add_job(create_order, 'interval', minutes=max(cooking_times),
                          args=(res.user, order_id, res.longitude, res.latitude, res.address, res.summa, scheduler, c.bot),
                          id=str(res.id))
    else:
        order_id = str(c.data).replace("ca", "")
        await c.message.edit_text(f"Buyurtma: #{order_id}\n"
                                  f"Bekor qilindi ❌")
        res = await get_order(order_id)
        msg = ""
        if res.user.lang == "uz":
            msg = f"Buyurtma #{order_id} bekor qilindi.\n" \
                  f"Uzur hozirda sizni buyurtmangizni qabul qila olmaymiz 😞"
        if res.user.lang == "ru":
            msg = f"Заказ #{order_id} отменен." \
                  f"Извините, сейчас мы не можем принять ваш заказ 😞"
        if res.user.lang == "tr":
            msg = f"#{order_id} siparişi iptal edildi." \
                  f"Şimdi siparişinizi kabul edemeyiz 😞"
        await c.bot.send_message(chat_id=res.user.user_id, text=msg)


