from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.callback_data import CallbackData
from backend.models import *
from utils.db_api.database import *


async def about_menu(lang):
    texts = []
    if lang == "uz":
        texts = ["Telegram", "Facebook", "Youtube", "Instagram", "Orqaga"]
    elif lang == "ru":
        texts = ["Telegram", "Facebook", "Youtube", "Instagram", "Back"]
    elif lang == "ru":
        texts = ["Телеграм", "Facebook", "Youtube", "Instagram", "Назад"]
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"{texts[0]}", url="http://t.me/DunyaBunya")],
            [InlineKeyboardButton(text=f"{texts[1]}", url="https://www.facebook.com/dunyabunya.uz")],
            [InlineKeyboardButton(text=f"{texts[2]}", url="https://youtube.com/")],
            [InlineKeyboardButton(text=f" {texts[3]}", url="https://instagram.com/")],
        ]
    )
    return markup


async def admin_conf_btn(order_id):
    btns = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton('✅ Qabul qilish', callback_data=f"co{order_id}"),
                                                 InlineKeyboardButton('❌ Bekor qilish', callback_data=f"ca{order_id}"),)
    return btns


async def go_search(lang):
    texts = []
    if lang == "uz":
        texts = ["Izlash"]
    elif lang == "ru":
        texts = ["Search"]
    elif lang == "ru":
        texts = ["Поиск"]
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"🔎 {texts[0]}", switch_inline_query_current_chat=""),
            ],
        ]
    )
    return markup


async def go_order(lang):
    texts = []
    if lang == "uz":
        texts = ["Xaridni boshlash"]
    elif lang == "ru":
        texts = ["Начать покупки"]
    elif lang == "tr":
        texts = ["Alışverişe başla"]
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"🛍 {texts[0]} ↗️", callback_data="go_shopping")],
        ]
    )
    return markup


async def category_keyboard(lang, user_id=None):
    texts = []
    cart = False
    carts = await get_carts(user_id)
    categories = Category.objects.all()
    markup = InlineKeyboardMarkup(row_width=2)
    if carts not in  ["⚠️ Hozircha savatingiz bo'sh", '⚠️ Sepetiniz boş', '⚠️ Ваша корзина пуста.']:
        cart = True
        if lang == 'uz':
            markup.add(InlineKeyboardButton(text=f"🛒 Savatcha", callback_data=f"go_cart"))
        if lang == "tr":
            markup.add(InlineKeyboardButton(text=f"🛒 Alışveriş Sepeti", callback_data=f"go_cart"))
        if lang == "ru":
            markup.add(InlineKeyboardButton(text=f"🛒 Корзина", callback_data=f"go_cart"))
            
    for i in categories:
        if lang == "uz":
            if cart:
                markup.row(InlineKeyboardButton(text=f"{i.name_uz}", callback_data=i.id))
                cart = False
            else:    
                markup.insert(InlineKeyboardButton(text=f"{i.name_uz}", callback_data=i.id))
            texts = ["Orqaga"]
        elif lang == "ru":
            if cart:
                markup.row(InlineKeyboardButton(text=f"{i.name_ru}", callback_data=i.id))
                cart = False
            else:
                markup.insert(InlineKeyboardButton(text=f"{i.name_ru}", callback_data=i.id))
            texts = ["Назад"]
        elif lang == "tr":
            if cart:
                markup.row(InlineKeyboardButton(text=f"{i.name_tr}", callback_data=i.id))
                cart = False
            else:
                markup.insert(InlineKeyboardButton(text=f"{i.name_tr}", callback_data=i.id))
            texts = ["Geri"]
    markup.add(InlineKeyboardButton(text=f"🔙 {texts[0]}", callback_data=f"back"))
    return markup


async def product_keyboard(lang, cat_id):
    texts = ''
    products = Product.objects.filter(category__id=cat_id, stop_list=False).all()
    inline_keyboard = []
    keyboard = InlineKeyboardMarkup(row_width=2)
    for i in products:
        if lang == "uz":
            # inline_keyboard.append([InlineKeyboardButton(text=f"{i.name_uz}", callback_data=i.id)])
            keyboard.insert(InlineKeyboardButton(text=f"{i.name_uz}", callback_data=i.id))
            texts = "Orqaga"
        elif lang == "ru":
            # inline_keyboard.append([InlineKeyboardButton(text=f"{i.name_ru}", callback_data=i.id)])
            keyboard.insert(InlineKeyboardButton(text=f"{i.name_ru}", callback_data=i.id))
            texts = "Назад"
        elif lang == "tr":
            # inline_keyboard.append([InlineKeyboardButton(text=f"{i.name_tr}", callback_data=i.id)])
            keyboard.insert(InlineKeyboardButton(text=f"{i.name_tr}", callback_data=i.id))
            texts = "Geri"
    inline_keyboard.append([InlineKeyboardButton(text=f"🔙 {texts}", callback_data=f"back")])
    keyboard.add(InlineKeyboardButton(text=f"🔙 {texts}", callback_data=f"back"))
    markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard, row_width=3)
    return keyboard


async def order_keyboard(lang, cart_id):
    texts = []
    if lang == "uz":
        texts = ["Savatchaga qo'shish", "Orqaga"]
    elif lang == "ru":
        texts = ["Добавить в корзину", "Назад"]
    elif lang == "tr":
        texts = ["Sepete ekle", "Geri"]

    markup = InlineKeyboardMarkup(row_width=3)
    cart = CartObject.objects.filter(id=cart_id).first()
    markup.insert(
        InlineKeyboardButton(text=f"➖", callback_data=f"cart_minus-{cart.id}"))
    markup.insert(
        InlineKeyboardButton(text=f"{cart.count}", callback_data="no_call-1"))
    markup.insert(
        InlineKeyboardButton(text=f"➕", callback_data=f"cart_plus-{cart.id}"))
    markup.row(InlineKeyboardButton(text=f"📥 {texts[0]} ", callback_data=f"confirm-{cart.id}"))
    markup.row(InlineKeyboardButton(text=f"⬅️ {texts[1]} ", callback_data=f"cancel-{cart.id}"))
    return markup


# async def product_count_keyboard(lang, cart_id):
#     texts = []
#     if lang == "uz":
#         texts = ["Savatchaga qo'shish", "Orqaga"]
#     elif lang == "ru":
#         texts = ["Add to card", "Back"]
#     elif lang == "ru":
#         texts = ["Добавить в корзину", "Назад"]

#     markup = InlineKeyboardMarkup(row_width=3)
#     cart = CartObject.objects.filter(id=cart_id).first()
#     markup.insert(
#         InlineKeyboardButton(text=f"➖", callback_data=f"cart_minus-{cart.id}"))
#     markup.insert(
#         InlineKeyboardButton(text=f"{cart.count}", callback_data="no_call-1"))
#     markup.insert(
#         InlineKeyboardButton(text=f"➕", callback_data=f"cart_plus-{cart.id}"))
#     markup.row(InlineKeyboardButton(text=f"📥 {texts[0]} ", callback_data=f"confirm-{cart.id}"))
#     markup.row(InlineKeyboardButton(text=F"⬅️ {texts[1]} ", callback_data=f"cancel-{cart.id}"))
#     return markup



# async def back_admin_menu():
#     markup = InlineKeyboardMarkup(
#         inline_keyboard=[
#             [
#                 InlineKeyboardButton(text="🔙 Orqaga", callback_data=f"back_admin"),
#             ],
#         ]
#     )
#     return markup


# async def doctor_in_admin():
#     markup = InlineKeyboardMarkup(
#         inline_keyboard=[
#             [InlineKeyboardButton(text="🗓 Bugungi kungi keshbekni ko'rish", callback_data="kash_today")],
#             [InlineKeyboardButton(text="📅 Alohida kun uchun keshbekni ko'rish", callback_data="kash_day")],
#             [InlineKeyboardButton(text="📆 Shu oy uchun keshbekni ko'rish", callback_data="kash_this_month")],
#             [InlineKeyboardButton(text="🗒 Alohida oy uchun keshbekni ko'rish", callback_data="kash_month")],
#             [InlineKeyboardButton(text="🔙 Orqaga", callback_data=f"back_admin")],
#         ]
#     )
#     return markup


# async def back_keyboard():
#     keyboard = ReplyKeyboardMarkup()
#     key1 = KeyboardButton(text="⬅️ Bekor qilish")
#     keyboard.add(key1)
#     keyboard.resize_keyboard = True
#     return keyboard


# async def ask_keyboard():
#     keyboard = ReplyKeyboardMarkup()
#     key1 = KeyboardButton(text="💵 Avans so'rash")
#     keyboard.add(key1)
#     keyboard.resize_keyboard = True
#     return keyboard


# async def admin_menu():
#     keyboard = ReplyKeyboardMarkup(row_width=2)
#     key1 = KeyboardButton(text="Eslatma qo'shish")
#     keyboard.add(key1)
#     keyboard.resize_keyboard = True
#     return keyboard

# async def client_keys():
#     keyboard = ReplyKeyboardMarkup(row_width=2)
#     key1 = KeyboardButton(text="Keyingi to'lovni ko'rish")
#     keyboard.add(key1)
#     keyboard.resize_keyboard = True
#     return keyboard
