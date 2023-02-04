from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.callback_data import CallbackData
from backend.models import *
from utils.db_api.database import *


async def settings_keyboard(lang):
    texts = []
    if lang == "uz":
        texts = ["Raqamni o'zgartirish", "Tilni o'zgartirish", "Orqaga"]
    elif lang == "ru":
        texts = ["Изменить номер телефона", "Изменить язык", "Назад"]
    else:
        texts = ["Telefon numarasını değiştir", "Dili değiştir", "Geri"]
    keyboard = ReplyKeyboardMarkup()
    key1 = KeyboardButton(text=f"📞 {texts[0]}")
    key2 = KeyboardButton(text=f"🔄 {texts[1]}")
    key_back = KeyboardButton(text=f"⬅️️ {texts[2]}")
    keyboard.add(key1, key2)
    keyboard.add(key_back)
    keyboard.resize_keyboard = True
    return keyboard


async def comment_keyboard(lang):
    texts = []
    if lang == "uz":
        texts = ["Izoh qo'shish", "Tashlab ketish", "Orqaga"]
    elif lang == "ru":
        texts = ["Добавить комментарий", "Пропустить", "Назад"]
    else:
        texts = ["Yorum ekle", "Atlamak", "Geri"]
    keyboard = ReplyKeyboardMarkup()
    key1 = KeyboardButton(text=f"💬 {texts[0]}")
    key2 = KeyboardButton(text=f"➡️ {texts[1]}")
    key_back = KeyboardButton(text=f"⬅️️ {texts[2]}")
    keyboard.add(key1, key2)
    keyboard.add(key_back)
    keyboard.resize_keyboard = True
    return keyboard


async def phone_keyboard(lang):
    texts = []
    if lang == "uz":
        texts = ["Raqamni ulashish", "Orqaga"]
    elif lang == "ru":
        texts = ["Отправить номер телефона", "Назад"]
    else:
        texts = ["Telefon numarasını gönder", "Geri"]
    keyboard = ReplyKeyboardMarkup()
    key1 = KeyboardButton(text=f"📞 {texts[0]}", request_contact=True)
    key2 = KeyboardButton(text=f"⬅️️ {texts[1]}")
    keyboard.add(key1)
    keyboard.add(key2)
    keyboard.resize_keyboard = True
    return keyboard


async def language_keyboard():
    keyboard = ReplyKeyboardMarkup()
    key1 = KeyboardButton(text="🇺🇿 O'zbek tili")
    key2 = KeyboardButton(text="🇷🇺 Pусский язык")
    key3 = KeyboardButton(text="🇹🇷 Türk")
    keyboard.add(key1, key2, key3)
    keyboard.resize_keyboard = True
    return keyboard


async def user_menu(lang):
    texts = []
    if lang == "uz":
        texts = ["Buyurtma berishs", "Sozlamalar", "Biz haqimizda", "Fikr qoldirish", "Savat", "Buyurtmalar tarixi"]
    elif lang == "ru":
        texts = ["Заказать сейчас", "Настройки", "О нас", "Обратная связь", "Корзина", "История заказов"]
    else:
        texts = ["Şimdi sipariş ver", "Ayarlar", "Hakkımızda", "Geribildirim", "Alışveriş Sepeti", "Satın alım geçmişi"]

    keyboard = ReplyKeyboardMarkup()
    key1 = KeyboardButton(text=f"🛍 {texts[0]}")
    key2 = KeyboardButton(text=f"⚙️ {texts[1]}")
    # key3 = KeyboardButton(text=f"ℹ️ {texts[2]}")
    key4 = KeyboardButton(text=f"✍️ {texts[3]}")
    key5 = KeyboardButton(text=f"📥  {texts[4]}")
    key6 = KeyboardButton(text=f"🗂 {texts[5]}")
    keyboard.add(key1)
    keyboard.add(key5, key6)
    keyboard.add(key2, key4)
    keyboard.resize_keyboard = True
    keyboard.one_time_keyboard = True
    return keyboard


async def back_keyboard(lang):
    texts = []
    if lang == "uz":
        texts = ["Orqaga"]
    elif lang == "ru":
        texts = ["Назад"]
    elif lang == "tr":
        texts = ["Geri"]

    keyboard = ReplyKeyboardMarkup()
    key1 = KeyboardButton(text=f"⬅️️ {texts[0]}")
    keyboard.add(key1)
    keyboard.resize_keyboard = True
    return keyboard


async def order_type(lang):
    texts = []
    if lang == "uz":
        texts = ["Olib ketish", "Yetkazib berish", "Orqaga"]
    elif lang == "ru":
        texts = ["Самовывоз", "Доставка", "Назад"]
    elif lang == "tr":
        texts = ["Götürmek", "Teslimat", "Geri"]

    keyboard = ReplyKeyboardMarkup()
    key1 = KeyboardButton(text=f"🏃‍♂️ {texts[0]}")
    key2 = KeyboardButton(text=f"🚚 {texts[1]}")
    key3 = KeyboardButton(text=f"⬅️ {texts[2]}")
    keyboard.add(key2, key1)
    keyboard.add(key3)
    keyboard.resize_keyboard = True
    return keyboard


async def cart_keyboard(lang, user_id):
    user = User.objects.filter(user_id=user_id).first()
    texts = []
    carts = CartObject.objects.filter(user=user, confirm=True).all()
    keyboard = ReplyKeyboardMarkup()
    for i in carts:
        if lang == "uz":
            texts = ["Asosiy menyu", "Orqaga", "Savatchani tozalash", "Buyurtmani rasmiylashtirish"]
            keyboard.add(KeyboardButton(text=f"❌ {i.product.name_uz}"))
        elif lang == "ru":
            texts = ["Главное меню", "Назад", "Очистить корзину", "Оформить заказ"]
            keyboard.add(KeyboardButton(text=f"❌ {i.product.name_ru}"))
        elif lang == "tr":
            texts = ["Ana menü", "Geri", "Çöp kutusunu boşalt", "Siparişi tamamlayın"]
            keyboard.add(KeyboardButton(text=f"❌ {i.product.name_tr}"))
    back_key = KeyboardButton(f"⬅️ {texts[1]}")
    home_key = KeyboardButton(f"🏠 {texts[0]}")
    clear_key = KeyboardButton(f"🗑 {texts[2]}")
    order_key = KeyboardButton(f"🛒 {texts[3]}")
    keyboard.add(clear_key, order_key)  
    keyboard.add(back_key, home_key)  
    keyboard.resize_keyboard = True
    return keyboard


async def pay_method(lang):
    texts = []
    if lang == "uz":
        texts = ["Click", "Payme", "Naqd pul orqali" , "Orqaga"]
    elif lang == "ru":
        texts = ["Click", "Payme", "Наличные", "Назад"]
    elif lang == "tr":
        texts = ["Click", "Payme", "Nakit", "Geri"]

    keyboard = ReplyKeyboardMarkup()
    key1 = KeyboardButton(text=f"🔵 {texts[0]}")
    # key2 = KeyboardButton(text=f"🟢 {texts[1]}")
    key3 = KeyboardButton(text=f"💴 {texts[2]}")
    key4 = KeyboardButton(text=f"⬅️ {texts[3]}")
    keyboard.add(key1, key3)
    keyboard.add(key4)
    keyboard.resize_keyboard = True
    return keyboard


async def location_send(lang):
    text = []
    if lang == 'uz':
        text = ['Joylashuvni ulashish', 'Oldingi manzillar', "Orqaga"]
    elif lang == 'ru':
        text = ['Отправить местоположение', 'Предыдущие адреса', "Назад"]
    elif lang == 'tr':
        text = ['Konum gönder', 'Önceki adresler', "Geri"]
    mrk = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    bt = KeyboardButton(f'📍 {text[0]}', request_location=True)
    back_key = KeyboardButton(f"⬅️ {text[2]}")
    btn = KeyboardButton(f'🔂 {text[1]}')
    mrk.add(bt, btn)
    mrk.add(back_key)
    return mrk


async def product_back_keyboard(lang):      
    texts = []
    keyboard = ReplyKeyboardMarkup()
    if lang == "uz":
        texts = ["Asosiy menyu", "Orqaga"]
    elif lang == "ru":
        texts = ["Главное меню", "Назад"]
    elif lang == "tr":
        texts = ["Ana menü", "Geri"]
    back_key = KeyboardButton(f"⬅️ {texts[1]}")
    home_key = KeyboardButton(f"🏠 {texts[0]}")
    keyboard.add(back_key, home_key)  
    keyboard.resize_keyboard = True
    return keyboard


async def confirm_address(lang):
    text = []
    if lang == 'uz':
        text = ['Tasdiqlash', 'Qayta jo\'natish', 'Orqaga']
    elif lang == 'ru':
        text = ['Подтвердить', 'Отправить повторно', 'Назад']
    elif lang == 'tr':
        text = ['Onayla', 'Tekrar gönderin', 'Geri']
    markup =     keyboard = ReplyKeyboardMarkup()
    key1 = KeyboardButton(text=f"✅ {text[0]}")
    key2 = KeyboardButton(f"🔄 {text[1]}")
    back_key = KeyboardButton(f"⬅️ {text[2]}")
    keyboard.add(key1, key2)  
    keyboard.add(back_key)
    keyboard.resize_keyboard = True
    return markup


async def location_keys(user_id, lang):
    locs = await get_address(user_id)
    keyboard = ReplyKeyboardMarkup()
    for i in locs:
        if lang == "uz":
            texts = ['Orqaga']
            keyboard.add(KeyboardButton(text=f"{i.name}"))
        elif lang == "ru":
            texts = ['Back']
            keyboard.add(KeyboardButton(text=f"{i.name}"))
        elif lang == "tr":
            texts = ['Geri']
            keyboard.add(KeyboardButton(text=f"{i.name}"))
    back_key = KeyboardButton(f"⬅️ {texts[0]}")
    keyboard.add(back_key)  
    keyboard.resize_keyboard = True
    return keyboard


async def order_confirmation(lang):
    texts = []
    if lang == "uz":
        texts = ["Buyurtmani tasdiqlash", "Bekor qilish"]
    elif lang == "ru":
        texts = ["Подтвердить заказ", "Отмена"]
    elif lang == "tr":
        texts = ["Sipariş onaylamak", "İptal"]
        
    keyboard = ReplyKeyboardMarkup()
    key1 = KeyboardButton(text=f"✅ {texts[0]}")
    key2 = KeyboardButton(text=f"❌ {texts[1]}")
    keyboard.add(key1, key2)
    keyboard.resize_keyboard = True
    return keyboard


async def confirmation_keyboard(lang):
    texts = []
    if lang == "uz":
        texts = ["Tasdiqlash", "Bekor qilish"]
    elif lang == "ru":
        texts = ["Подтвердить", "Отмена"]
    elif lang == "tr":
        texts = ["Onaylamak", "İptal"]

    keyboard = ReplyKeyboardMarkup()
    key1 = KeyboardButton(text=f"✅ {texts[0]}")
    key2 = KeyboardButton(text=f"❌ {texts[1]}")
    keyboard.add(key1, key2)
    keyboard.resize_keyboard = True
    return keyboard


# async def filial_keyboard(lang):
#     texts = []
#     filials = Filial.objects.all()
#     keyboard = ReplyKeyboardMarkup()
#     for i in filials:
#         if lang == "uz":
#             texts = ["Asosiy menyu", "Orqaga"]
#             keyboard.add(KeyboardButton(text=f"{i.filial_uz}"))
#         elif lang == "ru":
#             texts = ["Главное меню", "Back"]
#             keyboard.add(KeyboardButton(text=f"{i.filial_en}"))
#         elif lang == "tr":
#             texts = ["Ana menü", "Geri"]
#             keyboard.add(KeyboardButton(text=f"{i.filial_tr}"))
#     back_key = KeyboardButton(f"⬅️ {texts[1]}")
#     home_key = KeyboardButton(f"🏠 {texts[0]}")
#     keyboard.add(back_key, home_key)  
#     keyboard.resize_keyboard = True
#     return keyboard



# async def confirm_keyboard():
#     markup = InlineKeyboardMarkup(
#         inline_keyboard=[
#             [
#                 InlineKeyboardButton(text="❌ Yo'q", callback_data=f"cancel"),
#                 InlineKeyboardButton(text="✅ Ha", callback_data=f"confirm"),
#             ],
#         ]
#     )
#     return markup


# async def get_or_back():
#     markup = InlineKeyboardMarkup(
#         inline_keyboard=[
#             [
#                 InlineKeyboardButton(text="🔙 Orqaga", callback_data=f"back"),
#                 InlineKeyboardButton(text="📑 Excell hujjatni yuklash", callback_data=f"get"),
#             ],
#         ]
#     )
#     return markup


# async def back_to():
#     markup = InlineKeyboardMarkup(
#         inline_keyboard=[
#             [
#                 InlineKeyboardButton(text="🔙 Orqaga", callback_data=f"back_to_menu"),
#             ],
#         ]
#     )
#     return markup


# async def year_keyboard(years):
#     inline_keyboard = []
#     for i in years:
#         inline_keyboard.append([InlineKeyboardButton(text=f"{i}", callback_data=i)])
#     inline_keyboard.append([InlineKeyboardButton(text="🔙 Orqaga", callback_data=f"back_menu")])
#     markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
#     return markup


# Moths = {1: 'Yanvar', 2: 'Fevral', 3: 'Mart', 4: 'Aprel', 5: 'May', 6: 'Iyun', 7: 'Iyul', 8: 'Avgust', 9: 'Sentabr',
#          10: 'Oktyabr', 11: 'Noyabr', 12: 'Dekabr', }


# async def month_keyboard(date):
#     inline_keyboard = []
#     for i in date:
#         inline_keyboard.append([InlineKeyboardButton(text=f"{Moths[i]}", callback_data=i)])
#     inline_keyboard.append([InlineKeyboardButton(text="🔙 Orqaga", callback_data=f"back_menu")])
#     markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
#     return markup
