from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.callback_data import CallbackData
from backend.models import *
from utils.db_api.database import *


async def admin_category_keyboard():
    
    categories = Category.objects.all()
    markup = InlineKeyboardMarkup(row_width=2)
    for i in categories:
        markup.insert(InlineKeyboardButton(text=f"{i.name_uz}", callback_data=i.id))
    markup.add(InlineKeyboardButton(text=f"🔙 Назад", callback_data=f"back"))
    return markup


async def admin_product_keyboard(cat_id):
    products = Product.objects.filter(category__id=cat_id).all()
    markup = InlineKeyboardMarkup(row_width=2)
    for i in products:
        if i.stop_list:
            markup.insert(InlineKeyboardButton(text=f"❌ {i.name_uz}", callback_data=i.id))
        else:
            markup.insert(InlineKeyboardButton(text=f"{i.name_uz}", callback_data=i.id))
    markup.add(InlineKeyboardButton(text=f"🔙 Назад", callback_data=f"back"))
    return markup

