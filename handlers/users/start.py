from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext

from handlers.users.taxi import create_order
from keyboards.inline.main_inline import *
from keyboards.inline.menu_button import *
from utils.db_api import database as commands
from loader import dp, bot
from utils.db_api.database import *
import datetime
from datetime import timedelta
from aiogram.types import ReplyKeyboardRemove
from geopy.geocoders import Nominatim
from aiogram.types import InlineQuery, \
    InputTextMessageContent, InlineQueryResultPhoto, InputMediaPhoto, InlineQueryResultArticle
import re 
import requests
from data import config


def send_sms(otp, phone):
    username = 'foodline'
    password = 'JvYkp44)-J&9'
    sms_data = {
        "messages":[{"recipient":f"{phone}","message-id":"abc000000003","sms":{"originator": "3700","content": {"text": f"Ваш код подтверждения для MUSTAFA TURKISH CUSINE BOT: {otp}"}}}]}
    url = "http://91.204.239.44/broker-api/send"
    res = requests.post(url=url, headers={}, auth=(username, password), json=sms_data)


def generateOTP():
    return random.randint(111111, 999999)

def isValid(s):
    Pattern = re.compile("(0|91)?[7-9][0-9]{9}")
    return Pattern.match(s)

# def send_sms(phone: int, message: str) -> dict:
#     api = SmsAero(SMSAERO_EMAIL, SMSAERO_API_KEY)
#     return api.send(phone, message)


@dp.message_handler(lambda message: message.text in ["🏠 Asosiy menyu", "🏠 Главное меню", "🏠 Ana menü"], state='*')
async def go_home(message: types.Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    markup = await user_menu(lang)
    if lang == "uz":
        await message.answer("Botimizga xush kelibsiz. Iltimos kerakli bo'limni tanlang 👇", reply_markup=markup)
    elif lang == "tr":
        await message.answer("Botumuza hoş geldiniz. İstediğiniz bölümü seçin👇", reply_markup=markup)
    elif lang == "ru":
        await message.answer("Добро пожаловать в наш бот. Пожалуйста, выберите нужный раздел 👇", reply_markup=markup)
    await state.set_state("get_command")
 

@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message, state: FSMContext):
    user = await get_user(message.from_id)
    if user is not None:
        lang = await get_lang(message.from_user.id)
        if user.phone is not None:
            markup = await user_menu(lang)
            if lang == "uz":
                await message.answer("Botimizga xush kelibsiz. Iltimos kerakli bo'limni tanlang 👇", reply_markup=markup)
            elif lang == "tr":
                await message.answer("Botumuza hoş geldiniz. İstediğiniz bölümü seçin👇", reply_markup=markup)
            elif lang == "ru":
                await message.answer("Добро пожаловать в наш бот. Пожалуйста, выберите нужный раздел 👇", reply_markup=markup)
            await state.set_state("get_command")
        else:
            markup = await phone_keyboard(lang)
            if lang == "uz":
                await message.answer("Telefon raqamininfizni xalqaro formatda(<b>998YYXXXXXXX</b>) kiriting. Yoki raqamni ulashing👇", reply_markup=markup)
            elif lang == "tr":
                await message.answer("Telefon numaranızı uluslararası biçimde girin (<b>998YYXXXXXX</b>). Veya numarayı paylaşın👇", reply_markup=markup)
            elif lang == "ru":
                await message.answer("Введите свой номер телефона в международном формате (<b>998YYXXXXXX</b>). Или поделитесь номером👇", reply_markup=markup)
            await state.set_state("get_phone_number")            
    else:
        markup =await language_keyboard()
        await message.answer(f"Assalomu alaykum, {message.from_user.first_name}👋. \nKerakli tilni tanlang 👇\n\nMerhaba {message.from_user.first_name}👋. \nİhtiyacınız olan dili seçin 👇\n\nЗдравствуйте, {message.from_user.first_name}👋. \nВыберите нужный язык 👇", 
                            reply_markup=markup)
        await state.set_state("get_lang")


@dp.message_handler(content_types=types.ContentTypes.CONTACT, state="get_phone_number")
async def get_phone(message: types.Message, state: FSMContext):
    if message.contact:
        # phone = message.contact.phone_number.split('+')
        phone = message.contact.phone_number[1:]
        print(phone)
        user = await get_user(message.from_user.id)
        user.new_phone = phone
        otp = generateOTP()
        send_sms(otp=otp, phone=phone)
        user.otp = otp
        user.save()
        lang = await get_lang(message.from_user.id)
        keyboard = await back_keyboard(lang)
        if lang == "uz":
            await message.answer(text=f"<b>{user.new_phone}</b> raqamiga yuborilgan tasdiqlash kodini kiriting", parse_mode='HTML', reply_markup=keyboard)
        if lang == "ru":
            await message.answer(text=f"Введите код подтверждения, отправленный на номер <b>{user.new_phone}</b>.", parse_mode='HTML', reply_markup=keyboard)
        if lang == "tr":
            await message.answer(text=f"<b>{user.new_phone}</b> adresine gönderilen doğrulama kodunu girin", parse_mode='HTML', reply_markup=keyboard)
        await state.set_state("get_otp")
    

@dp.message_handler(content_types=types.ContentTypes.TEXT, state="get_phone_number")
async def get_phone(message: types.Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    if "⬅️️" in message.text:
        user = await get_user(message.from_id)
        if user is not None:
            lang = await get_lang(message.from_user.id)
            if user.phone is not None:
                markup = await user_menu(lang)
                if lang == "uz":
                    await message.answer("Botimizga xush kelibsiz. Iltimos kerakli bo'limni tanlang 👇", reply_markup=markup)
                elif lang == "tr":
                    await message.answer("Botumuza hoş geldiniz. İstediğiniz bölümü seçin👇", reply_markup=markup)
                elif lang == "ru":
                    await message.answer("Добро пожаловать в наш бот. Пожалуйста, выберите нужный раздел 👇", reply_markup=markup)
                await state.set_state("get_command")
            else:
                markup = await phone_keyboard(lang)
                if lang == "uz":
                    await message.answer("Telefon raqamininfizni xalqaro formatda(<b>998YYXXXXXXX</b>) kiriting. Yoki raqamni ulashing👇", reply_markup=markup)
                elif lang == "tr":
                    await message.answer("Telefon numaranızı uluslararası biçimde girin (<b>998YYXXXXXX</b>). Veya numarayı paylaşın👇", reply_markup=markup)
                elif lang == "ru":
                    await message.answer("Введите свой номер телефона в международном формате (<b>998YYXXXXXX</b>). Или поделитесь номером👇", reply_markup=markup)
                await state.set_state("get_phone_number")            
        else:
            markup =await language_keyboard()
            await message.answer(f"Assalomu alaykum, {message.from_user.first_name}👋. \nKerakli tilni tanlang 👇\n\nHello, {message.from_user.first_name}👋. \nChoose the language you need 👇\n\nЗдравствуйте, {message.from_user.first_name}👋. \nВыберите нужный язык 👇", 
                                reply_markup=markup)
            await state.set_state("get_lang")
    else:
        if isValid(message.text):
            phone = message.text
            user = await get_user(message.from_user.id)
            user.new_phone = phone
            otp = generateOTP()
            send_sms(otp=otp, phone=phone)
            user.otp = otp
            user.save()
            keyboard = await back_keyboard(lang)
            if lang == "uz":
                await message.answer(text=f"<b>{user.new_phone}</b> raqamiga yuborilgan tasdiqlash kodini kiriting", parse_mode='HTML', reply_markup=keyboard)
            if lang == "ru":
                await message.answer(text=f"Введите код подтверждения, отправленный на номер <b>{user.new_phone}</b>.", parse_mode='HTML', reply_markup=keyboard)
            if lang == "tr":
                await message.answer(text=f"<b>{user.new_phone}</b> adresine gönderilen doğrulama kodunu girin", parse_mode='HTML', reply_markup=keyboard)
            await state.set_state("get_otp")
        else:
            markup = await phone_keyboard(lang)
            if lang == "uz":
                await message.answer("Telefon raqamininfizni xalqaro formatda(<b>998YYXXXXXXX</b>) kiriting. Yoki raqamni ulashing👇", reply_markup=markup)
            elif lang == "tr":
                await message.answer("Telefon numaranızı uluslararası biçimde girin (<b>998YYXXXXXX</b>). Veya numarayı paylaşın👇", reply_markup=markup)
            elif lang == "ru":
                await message.answer("Введите свой номер телефона в международном формате (<b>998YYXXXXXX</b>). Или поделитесь номером👇", reply_markup=markup)
            await state.set_state("get_phone_number")            
        

@dp.message_handler(content_types=types.ContentTypes.TEXT, state="get_otp")
async def get_phone(message: types.Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    lang = user.lang
    if "⬅️️" in message.text: 
        markup = await phone_keyboard(lang)
        if lang == "uz":
            await message.answer("Telefon raqamininfizni xalqaro formatda(<b>998YYXXXXXXX</b>) kiriting. Yoki raqamni ulashing👇", reply_markup=markup)
        elif lang == "tr":
            await message.answer("Telefon numaranızı uluslararası biçimde girin (<b>998YYXXXXXX</b>). Veya numarayı paylaşın👇", reply_markup=markup)
        elif lang == "ru":
            await message.answer("Введите свой номер телефона в международном формате (<b>998YYXXXXXX</b>). Или поделитесь номером👇", reply_markup=markup)
        await state.set_state("get_phone_number")            
    else:
        if message.text == user.otp:
            user.phone = user.new_phone
            user.save()
            markup = await user_menu(lang)
            if lang == "uz":
                await message.answer("Botimizga xush kelibsiz. Iltimos kerakli bo'limni tanlang 👇", reply_markup=markup)
            elif lang == "tr":
                await message.answer("Botumuza hoş geldiniz. İstediğiniz bölümü seçin👇", reply_markup=markup)
            elif lang == "ru":
                await message.answer("Добро пожаловать в наш бот. Пожалуйста, выберите нужный раздел 👇", reply_markup=markup)
            await state.set_state("get_command")
        else:
            lang = await get_lang(message.from_user.id)
            markup = await back_keyboard(lang)
            if lang == "uz":
                await message.answer("⚠️ Yuborilgan tasdiqlash kodi xato. Qayta urinib ko'ring", reply_markup=markup)
            elif lang == "tr":
                await message.answer("⚠️ Gönderilen doğrulama kodu hatalıdır. Tekrar deneyin", reply_markup=markup)
            elif lang == "ru":
                await message.answer("⚠️ Присланный проверочный код неверный. Попробуйте еще раз", reply_markup=markup)
            await state.set_state("get_otp")
        
    
@dp.message_handler(state="get_lang")
async def get_language(message: types.Message, state: FSMContext):
    if message.text in ["🇺🇿 O'zbek tili", "🇷🇺 Pусский язык", "🇹🇷 Türk"]:
        if message.text == "🇺🇿 O'zbek tili":
            data = "uz"
            await add_user(user_id=message.from_user.id, name=message.from_user.first_name, lang=data)
        elif message.text == "🇷🇺 Pусский язык":
            data = "ru"
            await add_user(user_id=message.from_user.id, name=message.from_user.first_name, lang=data)
        elif message.text == "🇹🇷 Türk":
            data = "tr"
            await add_user(user_id=message.from_user.id, name=message.from_user.first_name, lang=data)
        lang = await get_lang(message.from_user.id)
        markup = await phone_keyboard(lang)
        if lang == "uz":
            await message.answer("Telefon raqamininfizni xalqaro formatda(<b>998YYXXXXXXX</b>) kiriting. Yoki raqamni ulashing👇", reply_markup=markup)
        elif lang == "tr":
            await message.answer("Telefon numaranızı uluslararası biçimde girin (<b>998YYXXXXXX</b>). Veya numarayı paylaşın👇", reply_markup=markup)
        elif lang == "ru":
            await message.answer("Введите свой номер телефона в международном формате (<b>998YYXXXXXX</b>). Или поделитесь номером👇", reply_markup=markup)
        await state.set_state("get_phone_number")            
    else:
        markup =await language_keyboard()
        await message.answer(f"Kerakli tilni tanlang 👇\nВыберите нужный язык 👇\nGerekli dili seçin 👇", 
                            reply_markup=markup)
        await state.set_state("get_lang")
            

@dp.message_handler(lambda message: message.text in ["🛍 Buyurtma berish", "⚙️ Sozlamalar", "ℹ️ Biz haqimizda", "✍️ Fikr qoldirish", "🛍 Заказать сейчас", "⚙️ Настройки", "✍️ Обратная связь", "🛍 Şimdi sipariş ver", "⚙️ Ayarlar", "ℹ️ Hakkımızda", "✍️ Geribildirim", "📥  Savat", "📥  Корзина", "📥  Alışveriş Sepeti", "🗂 Buyurtmalar tarixi", "🗂 История заказов", "🗂 Satın alım geçmişi"], state="get_command")
async def get_user_command(message: types.Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    command = message.text
    if command in ["⚙️ Sozlamalar", "⚙️ Ayarlar", "⚙️ Настройки"]:
        markup = await settings_keyboard(lang)
        if lang == "uz":
            await message.answer(text="Kerakli buyruqni tanlang 👇", reply_markup=markup)
        elif lang == "tr":
            await message.answer(text="İstediğiniz komutu seçin 👇", reply_markup=markup)
        elif lang == "ru":
            await message.answer(text="Выберите нужную команду 👇", reply_markup=markup)
        await state.set_state("settings")
    elif command in ["✍️ Fikr qoldirish", "✍️ Обратная связь", "✍️ Geribildirim"]:
        lang = await get_lang(message.from_user.id)
        markup = await back_keyboard(lang)
        if lang == "uz":
            await message.answer("🖋 O'z fikr-mulohaza, shikoyat yoki takliflaringizni yozing. Yoki ovozli, video yoki foto xabar yuboring", reply_markup=markup)
        elif lang == "ru":
            await message.answer("🖋 Напишите свой отзыв, жалобу или пожелание. Или отправьте голосовое, видео или фото сообщение", reply_markup=markup)
        elif lang == "tr":
            await message.answer("🖋 Geri bildiriminizi, şikayetinizi veya dileğinizi yazın. Veya sesli, görüntülü veya fotoğraflı mesaj gönderin", reply_markup=markup)
        await state.set_state("get_feedback")      
    elif command in ["🛍 Buyurtma berish", "🛍 Заказать сейчас", "🛍 Şimdi sipariş ver"]:
        photo = open('./MAIN.jpg', 'rb')
        await message.answer(text=".", reply_markup=ReplyKeyboardRemove())
        markup = await category_keyboard(lang, message.from_user.id)
        if lang == "uz":
            await message.answer_photo(photo=photo, caption="Kerakli maxsulot kategoriyasini tanlang 👇", reply_markup=markup)
        elif lang == "ru":
            await message.answer_photo(photo=photo, caption="Выберите категорию еды 👇", reply_markup=markup)
        elif lang == "tr":
            await message.answer_photo(photo=photo, caption="İstediğiniz kategoriyi seçin 👇", reply_markup=markup)
        await state.update_data(order_type=order_type)
        message_id = int(message.message_id) + 1
        await bot.delete_message(message_id=message_id, chat_id=message.from_user.id)
        await state.set_state("get_category")
    elif command in ["📥  Savat", "📥  Корзина", "📥  Alışveriş Sepeti"]:
        text = await get_carts(message.from_id)
        if text is not None:
            cart_test = await check_cart(message.from_id)
            if cart_test:
                markup = await cart_keyboard(lang=lang, user_id=message.from_id)
                await message.answer(text=text, reply_markup=markup, parse_mode='HTML')
            else:
                go_m = await go_order(lang)
                markup = await back_keyboard(lang)
                if lang == "uz":
                    await message.answer(text, reply_markup=markup)
                    await message.answer("Xaridni boshlang ", reply_markup=go_m)
                elif lang == "tr":
                    await message.answer(text, reply_markup=markup)
                    await message.answer("Alışverişe başla", reply_markup=go_m)
                elif lang == "ru":
                    await message.answer(text, reply_markup=markup)
                    await message.answer("Начать покупки", reply_markup=go_m)
        await state.set_state("get_cart_command")
    elif command in ["🗂 Buyurtmalar tarixi", "🗂 История заказов", "🗂 Satın alım geçmişi"]:
        summa = 0
        orders = await get_orders(message.from_id)
        if lang =="uz":
            text = "<b>🛒Sizning Buyurtmalaringiz tarixi</b>\n\n"
        elif lang =="ru":
            text = "<b>🛒История ваших заказов</b>\n\n"
        elif lang =="tr":
            text = "<b>🛒Siparişlerinizin geçmişi</b>\n\n"
            
        for order in orders:
            summa = 0  
            order_details = await get_order_details(order.id)      
            if lang == "uz":
                text += f"🆔 Buyurtma: <b>#{order.id}</b>\n"\
                f"🕙Buyurtma vaqti: {order.date.year}-{order.date.month}-{order.date.day}  {order.date.hour}:{order.date.minute}\n📍 Manzil: {order.address}\n\n"
                for order_detail in order_details:
                    text += f"{order_detail.product.name_uz}✖️{order_detail.count}\n"
                    summa += order_detail.product.price * order_detail.count
                text += f"\n<b>Jami: </b>{summa} UZS\n\n"
            elif lang == "tr":
                text += f"<b>🛒Sipariş</b>\n\n🆔 Sipariş: <b>#{order.id}</b>\n"\
                f"🕙Sipariş zamanı: {order.date.year}-{order.date.month}-{order.date.day}  {order.date.hour}:{order.date.minute}\n📍 Adres: {order.address}\n\n"
                for order_detail in order_details:
                    text += f"{order_detail.product.name_tr}✖️{order_detail.count}\n"
                    summa += order_detail.product.price * order_detail.count
                text += f"\n<b>Toplam miktar: </b>{summa} UZS\n\n"
            elif lang == "ru":
                text = f"<b>🛒Ваш заказ</b>\n\n🆔 Заказ: <b>#{order.id}</b>\n"\
                f"🕙Дата заказа: {order.date.year}-{order.date.month}-{order.date.day}  {order.date.hour}:{order.date.minute}\n📍 Адрес: {order.address}\n\n"
                for order_detail in order_details:
                    text += f"{order_detail.product.name_ru}✖️{order_detail.count}\n"
                    summa += order_detail.product.price * order_detail.count
                text += f"\n<b>Общая сумма: </b>{summa} UZS\n\n"
        await message.answer(text)


@dp.message_handler(state="set_lang")
async def set_language(message: types.Message, state: FSMContext):
    data = message.text
    user = await get_user(message.from_user.id)
    if message.text == "🇺🇿 O'zbek tili":
        data = "uz"
    elif message.text == "🇷🇺 Pусский язык":
        data = "ru"
    elif message.text == "🇹🇷 Türk":
        data = "tr"
    user.lang = data
    user.save()
    lang = await get_lang(message.from_user.id)
    markup = await settings_keyboard(lang)
    if lang == "uz":
        await message.answer("Til o'zgariltirildi ✅.\nKerakli bo'limni tanlang 👇", reply_markup=markup)
    elif lang == "tr":
        await message.answer("Dil değiştirildi ✅.\nGerekli düğmeyi tıklayın👇", reply_markup=markup)
    elif lang == "ru":
        await message.answer("Язык изменен ✅.\nНажмите нужную кнопку👇", reply_markup=markup)
    await state.set_state("settings")


@dp.message_handler(content_types=types.ContentTypes.TEXT, state="settings")
async def get_settings_message(message: types.Message, state:FSMContext):
    lang = await get_lang(message.from_user.id)
    if "⬅️" in  message.text:
        markup = await user_menu(lang)
        if lang == "uz":
            await message.answer("Kerakli bo'limni tanlang 👇", reply_markup=markup)
        elif lang == "tr":
            await message.answer("Gerekli düğmeyi seçin👇", reply_markup=markup)
        elif lang == "ru":
            await message.answer("Выберите нужную кнопку👇", reply_markup=markup)
        await state.set_state("get_command")
    elif message.text in ["🔄 Tilni o'zgartirish", "🔄 Изменить язык", "🔄 Dili değiştir"]:
        if lang == "uz":
            markup = await language_keyboard()
            await message.answer(text="Tilni o'zgartirish ♻️\nKerakli tilni tanlang 👇", reply_markup=markup)
        elif lang == "tr":
            markup = await language_keyboard()
            await message.answer(text="Dili değiştir ♻️\nİstediğiniz dili seçin 👇", reply_markup=markup)
        elif lang == "ru":
            markup = await language_keyboard()
            await message.answer(text="Изменить язык ♻️\nВыберите нужный язык 👇", reply_markup=markup)
        await state.set_state("set_lang")
    elif message.text in ["📞 Raqamni o'zgartirish", "📞 Изменить номер телефона", "📞 Telefon numarasını değiştir"]:
        markup = await phone_keyboard(lang)
        if lang == "uz":
            await message.answer("Telefon raqamininfizni xalqaro formatda(<b>998YYXXXXXXX</b>) kiriting. Yoki raqamni ulashing👇", reply_markup=markup)
        elif lang == "tr":
            await message.answer("Telefon numaranızı uluslararası biçimde girin (<b>998YYXXXXXX</b>). Veya numarayı paylaşın👇", reply_markup=markup)
        elif lang == "ru":
            await message.answer("Введите свой номер телефона в международном формате (<b>998YYXXXXXX</b>). Или поделитесь номером👇", reply_markup=markup)
        await state.set_state("get_phone_number_settings")            


@dp.message_handler(content_types=types.ContentTypes.CONTACT, state="get_phone_number_settings")
async def get_phone(message: types.Message, state: FSMContext):
    if message.contact:
        phone = message.contact.phone_number.split('+')[1]
        user = await get_user(message.from_user.id)
        user.new_phone = phone
        otp = generateOTP()
        send_sms(otp=otp, phone=phone)
        user.otp = otp
        user.save()
        lang = await get_lang(message.from_user.id)
        keyboard = await back_keyboard(lang)
        if lang == "uz":
            await message.answer(text=f"<b>{user.new_phone}</b> raqamiga yuborilgan tasdiqlash kodini kiriting", parse_mode='HTML', reply_markup=keyboard)
        if lang == "ru":
            await message.answer(text=f"Введите код подтверждения, отправленный на номер <b>{user.new_phone}</b>.", parse_mode='HTML', reply_markup=keyboard)
        if lang == "tr":
            await message.answer(text=f"<b>{user.new_phone}</b> adresine gönderilen doğrulama kodunu girin", parse_mode='HTML', reply_markup=keyboard)
        await state.set_state("get_otp_settings")
    

@dp.message_handler(content_types=types.ContentTypes.TEXT, state="get_phone_number_settings")
async def get_phone(message: types.Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    if "⬅️️" in message.text:
        markup = await settings_keyboard(lang)
        if lang == "uz":
            await message.answer(text="Kerakli buyruqni tanlang 👇", reply_markup=markup)
        elif lang == "tr":
            await message.answer(text="İstediğiniz komutu seçin 👇", reply_markup=markup)
        elif lang == "ru":
            await message.answer(text="Выберите нужную команду 👇", reply_markup=markup)
        await state.set_state("settings")
    else:
        if isValid(message.text):
            phone = message.text
            user = await get_user(message.from_user.id)
            user.new_phone = phone
            otp = generateOTP()
            send_sms(otp=otp, phone=phone)
            user.otp = otp
            user.save()
            keyboard = await back_keyboard(lang)
            if lang == "uz":
                await message.answer(text=f"<b>{user.new_phone}</b> raqamiga yuborilgan tasdiqlash kodini kiriting", parse_mode='HTML', reply_markup=keyboard)
            if lang == "tr":
                await message.answer(text=f"Введите код подтверждения, отправленный на номер <b>{user.new_phone}</b>.", parse_mode='HTML', reply_markup=keyboard)
            if lang == "ru":
                await message.answer(text=f"<b>{user.new_phone}</b> adresine gönderilen doğrulama kodunu girin", parse_mode='HTML', reply_markup=keyboard)
            await state.set_state("get_otp_settings")
        else:
            markup = await phone_keyboard(lang)
            if lang == "uz":
                await message.answer("Telefon raqamininfizni xalqaro formatda(<b>998YYXXXXXXX</b>) kiriting. Yoki raqamni ulashing👇", reply_markup=markup)
            elif lang == "tr":
                await message.answer("Telefon numaranızı uluslararası biçimde girin (<b>998YYXXXXXX</b>). Veya numarayı paylaşın👇", reply_markup=markup)
            elif lang == "ru":
                await message.answer("Введите свой номер телефона в международном формате (<b>998YYXXXXXX</b>). Или поделитесь номером👇", reply_markup=markup)
            await state.set_state("get_phone_number_settings")            


@dp.message_handler(content_types=types.ContentTypes.TEXT, state="get_otp_settings")
async def get_phone(message: types.Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    lang = user.lang
    if "⬅️️" in message.text: 
        markup = await phone_keyboard(lang)
        if lang == "uz":
            await message.answer("Telefon raqamininfizni xalqaro formatda(<b>998YYXXXXXXX</b>) kiriting. Yoki raqamni ulashing👇", reply_markup=markup)
        elif lang == "tr":
            await message.answer("Telefon numaranızı uluslararası biçimde girin (<b>998YYXXXXXX</b>). Veya numarayı paylaşın👇", reply_markup=markup)
        elif lang == "ru":
            await message.answer("Введите свой номер телефона в международном формате (<b>998YYXXXXXX</b>). Или поделитесь номером👇", reply_markup=markup)
        await state.set_state("get_phone_number_settings")            
    else:
        if message.text == user.otp:
            user.phone = user.new_phone
            user.save()
            markup = await settings_keyboard(lang)
            if lang == "uz":
                await message.answer("✅ Telefon raqami o'zgartirildi. Iltimos kerakli bo'limni tanlang 👇", reply_markup=markup)
            elif lang == "tr":
                await message.answer("✅Telefon numarası değiştirilmiştir.. İstediğiniz bölümü seçin👇", reply_markup=markup)
            elif lang == "ru":
                await message.answer("✅ Номер телефона изменен. Пожалуйста, выберите нужный раздел 👇", reply_markup=markup)
            await state.set_state("settings")
        else:
            lang = await get_lang(message.from_user.id)
            markup = await back_keyboard(lang)
            if lang == "uz":
                await message.answer("⚠️ Yuborilgan tasdiqlash kodi xato. Qayta urinib ko'ring", reply_markup=markup)
            elif lang == "tr":
                await message.answer("⚠️ Gönderilen doğrulama kodu hatalıdır. Tekrar deneyin", reply_markup=markup)
            elif lang == "ru":
                await message.answer("⚠️ Присланный проверочный код неверный. Попробуйте еще раз", reply_markup=markup)
            await state.set_state("get_otp_settings")
                

@dp.message_handler(content_types=types.ContentTypes.PHOTO, state="get_feedback")
async def get_feedback_message(message: types.Message, state: FSMContext):
    await message.forward(chat_id=config.GROUPS_ID)
    lang = await get_lang(message.from_user.id)
    markup = await user_menu(lang)
    if lang == "uz":
        await message.answer("Fikr-mulohazangiz uchun tashakkur!", reply_markup=markup)
    elif lang == "tr":
        await message.answer("Geri bildiriminiz için teşekkür ederiz!", reply_markup=markup)
    elif lang == "ru":
        await message.answer("Спасибо за ваш отзыв!", reply_markup=markup)
    await state.set_state("get_command")

                
@dp.message_handler(state="get_feedback")
async def get_feedback_message(message: types.Message, state: FSMContext):
    if "⬅️" in message.text:
        lang = await get_lang(message.from_user.id)
        markup = await user_menu(lang)
        if lang == "uz":
            await message.answer("Kerakli bo'limni tanlang 👇", reply_markup=markup)
        elif lang == "tr":
            await message.answer("Gerekli düğmeyi seçin👇", reply_markup=markup)
        elif lang == "ru":
            await message.answer("Выберите нужную кнопку👇", reply_markup=markup)
        await state.set_state("get_command")
    else:
        if message.photo:
            await message.forward(chat_id=config.GROUPS_ID)
            await bot.forward_message(message_id=message.message_id, chat_id=config.GROUPS_ID, from_chat_id=message.from_user.id)
            lang = await get_lang(message.from_user.id)
            markup = await user_menu(lang)
            if lang == "uz":
                await message.answer("Fikr-mulohazangiz uchun tashakkur!", reply_markup=markup)
            elif lang == "tr":
                await message.answer("Geri bildiriminiz için teşekkür ederiz!", reply_markup=markup)
            elif lang == "ru":
                await message.answer("Спасибо за ваш отзыв!", reply_markup=markup)
            await state.set_state("get_command")
        else:
            await bot.forward_message(message_id=message.message_id, chat_id=config.GROUPS_ID, from_chat_id=message.from_user.id)
            lang = await get_lang(message.from_user.id)
            markup = await user_menu(lang)
            if lang == "uz":
                await message.answer("Fikr-mulohazangiz uchun tashakkur!", reply_markup=markup)
            elif lang == "tr":
                await message.answer("Geri bildiriminiz için teşekkür ederiz!", reply_markup=markup)
            elif lang == "ru":
                await message.answer("Спасибо за ваш отзыв!", reply_markup=markup)
            await state.set_state("get_command")
        

@dp.message_handler(state="get_command_about")
async def get_command_about(message: types.Message, state: FSMContext):
    if message.text in ["⬅️️️ Orqaga", "⬅️️️ Geri", "⬅️️️ Назад"]:
        lang = await get_lang(message.from_user.id)
        markup = await user_menu(lang)
        if lang == "uz":
            await message.answer("Kerakli bo'limni tanlang 👇", reply_markup=markup)
        elif lang == "tr":
            await message.answer("Gerekli düğmeyi seçin 👇", reply_markup=markup)
        elif lang == "ru":
            await message.answer("Выберите нужную кнопку 👇", reply_markup=markup)
        await state.set_state("get_command")


@dp.message_handler(state="get_service_type")
async def get_command_about(message: types.Message, state: FSMContext):
    user = await get_user(message.from_id)
    lang = await get_lang(message.from_user.id)
    if message.text in ["⬅️ Geri", "⬅️ Orqaga", "⬅️ Назад"]:
        text = await get_carts(message.from_id)
        if text is not None:
            cart_test = await check_cart(message.from_id)
            if cart_test:
                markup = await cart_keyboard(lang=lang, user_id=message.from_id)
                await message.answer(text=text, reply_markup=markup, parse_mode='HTML')
            else:
                go_m = await go_order(lang)
                markup = await back_keyboard(lang)
                if lang == "uz":
                    await message.answer(text, reply_markup=markup)
                    await message.answer("Xaridni boshlang ", reply_markup=go_m)
                elif lang == "ru":
                    await message.answer(text, reply_markup=markup)
                    await message.answer("Начать покупки", reply_markup=go_m)
                elif lang == "tr":
                    await message.answer(text, reply_markup=markup)
                    await message.answer("Alışverişe başla", reply_markup=go_m)
        await state.set_state("get_cart_command")
    elif message.text in ["🏃‍♂️ Olib ketish", "🏃‍♂️ Götürmek", "🏃‍♂️ Самовывоз"]:
        order_type = "pick"
        user.order_type = order_type
        user.save()
        date = datetime.datetime.now() + timedelta(hours=5)
        address = ''
        if lang == "uz":
            address = "Olib ketish"
        if lang == "tr":
            address = "Götürmek"
        if lang == "ru":
            address = "Самовывоз"
        order = await add_order(user_id=message.from_id, date=date, address=address)
        order.service_type = order_type
        await state.update_data(order_id=order.id)
        carts = await get_cart_objects(message.from_id)
        for cart in carts:
            await add_order_detail(order_id=order.id, product_id=cart.product.id, count=cart.count)
        order_deails = await get_order_details(order.id) 
        summa = 0
        dish = 0
        counts = 0
        markup = await order_confirmation(lang)
        if lang == "uz":
            text = f"<b>🛒Sizning Buyurtmangiz</b>\n\n🆔 Buyurtma: <b>#{order.id}</b>\n"\
            f"👤 Xaridor: <b>+{order.user.phone}</b>\n🕙Buyurtma vaqti: {order.date.year}-{order.date.month}-{order.date.day}  {order.date.hour}:{order.date.minute}\n📍 Manzil: {order.address}\n\n"
            for order_detail in order_deails:
                text += f"{order_detail.product.name_uz}✖️{order_detail.count}\n"
                counts += order_detail.count
                dish += order_detail.count * int(order_detail.product.dish)
                summa += order_detail.product.price * order_detail.count
            text += f"<b>Jami: </b>{summa} UZS\n"
            text += f"\n<b>Bir martalik idish uchun to'lov: </b>{counts} \nJami: {dish} UZS"
            summa += dish
            text += f"\n<b>Umumiy summa: </b>{summa} UZS"
        elif lang == "ru":
            text = f"<b>🛒Ваш заказ</b>\n\n🆔 Заказ: <b>#{order.id}</b>\n"\
            f"👤 Заказчик: <b>+{order.user.phone}</b>\n🕙Время заказа: {order.date.year}-{order.date.month}-{order.date.day}  {order.date.hour}:{order.date.minute}\n📍 Адрес: {order.address}\n\n"
            for order_detail in order_deails:
                text += f"{order_detail.product.name_ru}✖️{order_detail.count}\n"
                summa += order_detail.product.price * order_detail.count
                dish += order_detail.count * int(order_detail.product.dish)
                counts += order_detail.count
            text += f"<b>Общий: </b>{summa} UZS\n"    
            text += f"\n<b>Плата за одноразовую посуду: </b>{counts} \nОбщий: {dish} UZS"
            summa += dish
            text += f"\n<b>Общая сумма: </b>{summa} UZS"
        elif lang == "tr":
            text = f"<b>🛒Siparişiniz</b>\n\n🆔 Sipariş: <b>#{order.id}</b>\n"\
            f"👤 İstemci: <b>+{order.user.phone}</b>\n🕙Sipariş zamanı: {order.date.year}-{order.date.month}-{order.date.day}  {order.date.hour}:{order.date.minute}\n📍 Adres: {order.address}\n\n"
            for order_detail in order_deails:
                text += f"  {order_detail.product.name_uz}✖️{order_detail.count}\n"
                summa += order_detail.product.price * order_detail.count
                dish += order_detail.count * int(order_detail.product.dish)
                counts += order_detail.count
            text += f"<b>Total: </b>{summa} UZS\n"
            text += f"\n<b>Tek konteyner ücreti: </b>{counts} \nTotal: {dish} UZS"
            summa += dish
            text += f"\n<b>Toplam miktar: </b>{summa} UZS"
        order.summa = summa
        order.address = "Olib ketish"
        order.save()
        await message.answer(text, reply_markup=markup)
        await state.set_state("confirm_order")
    elif message.text in ["🚚 Yetkazib berish", "🚚 Доставка", "🚚 Teslimat"]:
        order_type = "deliver"
        user.order_type = order_type
        user.save()
        markup = await pay_method(lang)
        if lang == "uz":
            await message.answer("Iltimos to'lov usulini tanlang 👇", reply_markup=markup)
        elif lang == "tr":
            await message.answer("Lütfen bir ödeme yöntemi seçin 👇", reply_markup=markup)
        elif lang == "ru":
            await message.answer("Пожалуйста, выберите способ оплаты 👇", reply_markup=markup)
        await state.update_data(order_type=order_type)
        await state.set_state("get_payment_method")
    else:
        pass        


@dp.callback_query_handler(state="get_category")
async def get_command_about(call: types.CallbackQuery, state: FSMContext):
    lang = await get_lang(call.from_user.id)
    await call.message.delete()
    if call.data == 'back':
        markup = await user_menu(lang)
        if lang == "uz":
            await bot.send_message(chat_id=call.from_user.id, text="Botimizga xush kelibsiz. Iltimos kerakli bo'limni tanlang 👇", reply_markup=markup)
        elif lang == "tr":
            await bot.send_message(chat_id=call.from_user.id, text="Botumuza hoş geldiniz. İstediğiniz bölümü seçin👇", reply_markup=markup)
        elif lang == "ru":
            await bot.send_message(chat_id=call.from_user.id, text="Добро пожаловать в наш бот. Пожалуйста, выберите нужный раздел 👇", reply_markup=markup)
        await state.set_state("get_command")
    elif call.data == 'go_cart':
        text = await get_carts(call.from_user.id)
        if text not in  ['⚠️ Hozircha savatingiz bo\'sh', '⚠️ Sepetiniz boş', '⚠️ Your cart is currently empty']:
            markup = await cart_keyboard(lang=lang, user_id=call.from_user.id)
            await bot.send_message(chat_id=call.from_user.id, text=text, reply_markup=markup, parse_mode='HTML')
        else:
            go_m = await go_order(lang)
            markup = await back_keyboard(lang)
            await bot.send_message(chat_id=call.from_user.id, text=text, reply_markup=markup)
            if text == "ru":
                await bot.send_message(chat_id=call.from_user.id, text="Начать покупки", reply_markup=go_m)
            if text == "uz":
                await bot.send_message(chat_id=call.from_user.id, text="Xaridni boshlash", reply_markup=go_m)
            if text == "tr":
                await bot.send_message(chat_id=call.from_user.id, text="Alışverişe başla", reply_markup=go_m)
        await state.set_state("get_cart_command")
    else:
        category = await get_category(call.data)
        markup = await product_keyboard(lang=lang, cat_id=call.data)
        if category.image:
            photo = open(f'.{category.ImageURL}', 'rb')
            if lang == "uz":
                await bot.send_photo(chat_id=call.from_user.id, photo=photo, caption="Kerakli taomni tanlang 👇", reply_markup=markup)
            elif lang == "ru":
                await bot.send_photo(chat_id=call.from_user.id, photo=photo, caption="Выберите еду, которую вы хотите 👇", reply_markup=markup)
            elif lang == "tr":
                await bot.send_photo(chat_id=call.from_user.id, photo=photo, caption="İstediğiniz yemeği seçin 👇", reply_markup=markup)
        else:
            if lang == "uz":
                await bot.send_message(chat_id=call.from_user.id, text="Kerakli taomni tanlang 👇", reply_markup=markup)
            elif lang == "ru":
                await bot.send_message(chat_id=call.from_user.id, text="Выберите еду, которую вы хотите 👇", reply_markup=markup)
            elif lang == "tr":
                await bot.send_message(chat_id=call.from_user.id, text="İstediğiniz yemeği seçin 👇", reply_markup=markup)
        await state.set_state("get_product")
        

@dp.callback_query_handler(state="get_product")
async def get_command_about(call: types.CallbackQuery, state: FSMContext):
    lang = await get_lang(call.from_user.id)
    await call.message.delete()
    if call.data == 'back':
        photo = open('./MAIN.jpg', 'rb')
        markup = await category_keyboard(lang, user_id=call.from_user.id)
        if lang == "uz":
            await bot.send_photo(chat_id=call.from_user.id, photo=photo, caption="Kerakli kategoriyani tanlang 👇", reply_markup=markup)
        elif lang == "ru":
            await bot.send_photo(chat_id=call.from_user.id, photo=photo, caption="Выберите категорию еды 👇", reply_markup=markup)
        elif lang == "tr":
            await bot.send_photo(chat_id=call.from_user.id, photo=photo, caption="İstediğiniz kategoriyi seçin 👇", reply_markup=markup)
        await state.update_data(order_type=order_type)
        await state.set_state("get_category")
    else:
        product = await get_product(call.data)
        user = await get_user(call.from_user.id)
        cart = await add_cart(user=user, product=product)
        await state.update_data(cart_id=cart.id)
        markup = await order_keyboard(lang=lang, cart_id=cart.id)   
        if product.image:
            try:
                photo = open(f'.{product.ImageURL}', 'rb')
                if lang == "uz":
                    text = f"<b>{product.name_uz}</b>\n\n{product.description_uz}\n\nNarxi: <b>{product.price}</b>"
                    await bot.send_photo(chat_id=call.from_user.id, photo=photo, caption=text, reply_markup=markup)
                elif lang == "ru":
                    text = f"<b>{product.name_ru}</b>\n\n{product.description_ru}\n\nNarxi: <b>{product.price}</b>"
                    await bot.send_photo(chat_id=call.from_user.id, photo=photo, caption=text, reply_markup=markup)
                elif lang == "tr":
                    text = f"<b>{product.name_tr}</b>\n\n{product.description_tr}\n\nNarxi: <b>{product.price}</b>"
                    await bot.send_photo(chat_id=call.from_user.id, photo=photo, caption=text, reply_markup=markup)
            except:
                if lang == "uz":
                    text = f"<b>{product.name_uz}</b>\n\n{product.description_uz}\n\nNarxi: <b>{product.price}</b>"
                    await bot.send_message(chat_id=call.from_user.id, text=text, reply_markup=markup)
                elif lang == "ru":
                    text = f"<b>{product.name_ru}</b>\n\n{product.description_ru}\n\nNarxi: <b>{product.price}</b>"
                    await bot.send_message(chat_id=call.from_user.id, text=text, reply_markup=markup)
                elif lang == "tr":
                    text = f"<b>{product.name_tr}</b>\n\n{product.description_tr}\n\nNarxi: <b>{product.price}</b>"
                    await bot.send_message(chat_id=call.from_user.id, text=text, reply_markup=markup)
        else:
            if lang == "uz":
                text = f"<b>{product.name_uz}</b>\n\n{product.description_uz}\n\nNarxi: <b>{product.price}</b>"
                await bot.send_message(chat_id=call.from_user.id, text=text, reply_markup=markup)
            elif lang == "ru":
                text = f"<b>{product.name_ru}</b>\n\n{product.description_ru}\n\nNarxi: <b>{product.price}</b>"
                await bot.send_message(chat_id=call.from_user.id, text=text, reply_markup=markup)
            elif lang == "tr":
                text = f"<b>{product.name_tr}</b>\n\n{product.description_tr}\n\nNarxi: <b>{product.price}</b>"
                await bot.send_message(chat_id=call.from_user.id, text=text, reply_markup=markup)
        await state.set_state("cart_state")

    
@dp.callback_query_handler(state="cart_state")
async def cart_state(call: types.CallbackQuery, state: FSMContext):
    lang = await get_lang(call.from_user.id)
    command = call.data.split('-')[0]
    cart_id = call.data.split('-')[1]
    if command == "cancel":
        cart = await get_cart(cart_id)
        await call.message.delete()
        markup = await product_keyboard(lang, cat_id=cart.product.category.id)
        category = cart.product.category
        if category.image:
            photo = open(f'.{category.ImageURL}', 'rb')
            if lang == "uz":
                await bot.send_photo(chat_id=call.from_user.id, photo=photo, caption="Kerakli taomni tanlang 👇", reply_markup=markup)
            elif lang == "ru":
                await bot.send_photo(chat_id=call.from_user.id, photo=photo, caption="Выберите еду, которую вы хотите 👇", reply_markup=markup)
            elif lang == "tr":
                await bot.send_photo(chat_id=call.from_user.id, photo=photo, caption="İstediğiniz yemeği seçin 👇", reply_markup=markup)
        else:
            if lang == "uz":
                await bot.send_message(chat_id=call.from_user.id, text="Kerakli taomni tanlang 👇", reply_markup=markup)
            elif lang == "ru":
                await bot.send_message(chat_id=call.from_user.id, text="Выберите еду, которую вы хотите 👇", reply_markup=markup)
            elif lang == "tr":
                await bot.send_message(chat_id=call.from_user.id, text="İstediğiniz yemeği seçin 👇", reply_markup=markup)
        await state.set_state("get_product")
    elif command == "cart_plus":
        cart = await get_cart(cart_id)
        cart.count += 1
        cart.save()
        markup = await order_keyboard(lang=lang, cart_id=cart.id)
        if lang == "uz":
            await call.message.edit_reply_markup(reply_markup=markup)
        elif lang == "ru":
            await call.message.edit_reply_markup(reply_markup=markup)
        elif lang == "tr":
            await call.message.edit_reply_markup(reply_markup=markup)
    elif command == "cart_minus":
        cart = await get_cart(cart_id)
        if cart.count <= 1:
            cart.count = 1
        else:
            cart.count -= 1
        cart.save()
        markup = await order_keyboard(lang=lang, cart_id=cart.id)
        if lang == "uz":
            await call.message.edit_reply_markup(reply_markup=markup)
        elif lang == "ru":
            await call.message.edit_reply_markup(reply_markup=markup)
        elif lang == "tr":
            await call.message.edit_reply_markup(reply_markup=markup)
    elif command == "confirm":
        cart = await get_cart(cart_id)
        cart.confirm = True
        cart.save()
        await call.message.delete()
        markup = await category_keyboard(lang, user_id=call.from_user.id)
        if lang == "uz":
            await bot.send_message(chat_id=call.from_user.id, text="Buyurtma savatga qo'shildi✅.\nKerakli kategoriyani tanlang 👇", reply_markup=markup)
        elif lang == "ru":
            await bot.send_message(chat_id=call.from_user.id, text="Заказ добавлен в корзину.\n Выберите нужную категорию 👇", reply_markup=markup)
        elif lang == "tr":
            await bot.send_message(chat_id=call.from_user.id, text="Sipariş sepete eklendi.\nİstediğiniz kategoriyi seçin 👇", reply_markup=markup)
        await state.set_state("get_category")
        

@dp.callback_query_handler(state="get_cart_command")
async def get_cart_query(call:types.CallbackQuery, state:FSMContext):
    lang = await get_lang(call.from_user.id)
    await call.message.delete()
    markup = await category_keyboard(lang, user_id=call.from_user.id)
    photo = open('./MAIN.jpg', 'rb')
    if lang == "uz":
        await bot.send_photo(chat_id=call.from_user.id, photo=photo, caption="Kerakli maxsulot kategoriyasini tanlang 👇", reply_markup=markup)
    elif lang == "ru":
        await bot.send_photo(chat_id=call.from_user.id, photo=photo, caption="Выберите категорию еды 👇", reply_markup=markup)
    elif lang == "tr":
        await bot.send_photo(chat_id=call.from_user.id, photo=photo, caption="İstediğiniz kategoriyi seçin 👇", reply_markup=markup)
    await state.update_data(order_type=order_type)
    await state.set_state("get_category")
    

@dp.message_handler(state="get_cart_command")
async def get_count(message: types.Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    if "⬅️" in message.text:
        markup = await user_menu(lang)
        if lang == "uz":
            await message.answer("Botimizga xush kelibsiz. Iltimos kerakli bo'limni tanlang 👇", reply_markup=markup)
        elif lang == "ru":
            await message.answer("Добро пожаловать в наш бот. Выберите нужный раздел👇", reply_markup=markup)
        elif lang == "tr":
            await message.answer("Botumuza hoş geldiniz. Lütfen istediğiniz bölümü seçin 👇", reply_markup=markup)
        await state.set_state("get_command")
    elif message.text in ["🗑 Savatchani tozalash", "🗑 Çöp kutusunu boşalt", "🗑 Очистить корзину"]:
        await clear_cart(message.from_id)
        markup = await user_menu(lang)
        if lang == "uz":
            await message.answer("🗑 Savatcha tozalandi. Iltimos kerakli bo'limni tanlang 👇", reply_markup=markup)
        elif lang == "ru":
            await message.answer("🗑 Корзина очищена. Выберите нужный раздел👇", reply_markup=markup)
        elif lang == "tr":
            await message.answer("🗑 Sepet temizlendi. Lütfen istediğiniz bölümü seçin 👇", reply_markup=markup)
        await state.set_state("get_command")
    elif message.text in ["🛒 Buyurtmani rasmiylashtirish", "🛒 Siparişi tamamlayın", "🛒 Оформить заказ"]:
        markup = await order_type(lang)
        if lang == "uz":
            await message.answer(text="Xizmat turini tanlang", reply_markup=markup)
        elif lang == "tr":
            await message.answer(text="Hizmet türünü seçin", reply_markup=markup)
        elif lang == "ru":
            await message.answer(text="Выберите тип услуги", reply_markup=markup)
        await state.set_state("get_service_type")
    else:
        product_name = message.text.split("❌ ")
        try:
            product = await get_product_by_name(product_name[1])
        except:
            pass
        if product is not None:
            await delete_cart_item(product=product, user_id=message.from_user.id)
            text = await get_carts(message.from_id)
            markup = await user_menu(lang)
            if text not in ["⚠️ Hozircha savatingiz bo'sh", '⚠️ Sepetiniz boş', '⚠️ Ваша корзина пуста.']:
                markup = await cart_keyboard(lang=lang, user_id=message.from_id)
                await message.answer(text=text, reply_markup=markup, parse_mode='HTML')
                await state.set_state("get_cart_command")
            else:
                if lang == "uz":
                    await message.answer("❌ Savatchangiz bo'sh. Iltimos kerakli bo'limni tanlang 👇", reply_markup=markup)
                elif lang == "tr":
                    await message.answer("❌ Ваша корзина пуста. Выберите нужный раздел👇", reply_markup=markup)
                elif lang == "ru":
                    await message.answer("❌ Ваша корзина пуста. Пожалуйста, выберите нужный раздел 👇", reply_markup=markup)
                await state.set_state("get_command")


@dp.message_handler(state="get_payment_method")
async def get_count(message: types.Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    text = ''
    data = await state.get_data()
    user = await get_user(message.from_id)
    order_type = user.order_type
    if "⬅️" in message.text:
        text = await get_carts(message.from_id)
        if text is not None:
            markup = await cart_keyboard(lang=lang, user_id=message.from_id)
            await message.answer(text=text, reply_markup=markup, parse_mode='HTML')
            await state.set_state("get_cart_command")            
    elif message.text in ["🔵 Click", "🟢 Payme"]:
        card_type = ''
        if message.text == "🔵 Click":
            card_type = "click"
        elif message.text == "🟢 Payme":
            card_type = "payme"
        await state.update_data(card_type=card_type)
        if order_type == "deliver":
            lang = await get_lang(message.from_user.id)
            text = []
            if lang == 'uz':
                text = ['Yetkazish manzilini jo\'nating']
            elif lang == 'ru':
                text = ['Отправьте адрес доставки']
            elif lang == 'tr':
                text = ['Lütfen teslimat adresinizi gönderiniz']
            markup = await location_send(lang)
            await message.answer(text=f"{text[0]} 👇", reply_markup=markup)
            await state.set_state("get_address")
    elif message.text in ["💴 Naqd pul orqali", "💴 Наличные", "💴 Nakit"]:
        cash_type = "cash"
        if order_type == "deliver":
            lang = await get_lang(message.from_user.id)
            text = []
            if lang == 'uz':
                text = ['Yetkazish manzilini jo\'nating']
            elif lang == 'ru':
                text = ['Отправьте адрес доставки']
            elif lang == 'tr':
                text = ['Lütfen teslimat adresinizi gönderin']
            markup = await location_send(lang)
            await state.update_data(card_type=cash_type)
            await message.answer(f"{text[0]} 👇", reply_markup=markup)
            await state.set_state("get_address")
        else:
            order_type = "pick"
            date = datetime.datetime.now() + timedelta(hours=5)
            order = await add_order(user_id=message.from_id, date=date, address="Olib ketish")
            order.service_type = order_type
            await state.update_data(order_id=order.id)
            carts = await get_cart_objects(message.from_id)
            for cart in carts:
                await add_order_detail(order_id=order.id, product_id=cart.product.id, count=cart.count)
            order_deails = await get_order_details(order.id) 
            summa = 0
            markup = await order_confirmation(lang)
            if lang == "ru":
                text = f"<b>🛒Ваш заказ</b>\n\n🆔 Заказ: <b>#{order.id}</b>\n"\
                f"👤 Заказчик: <b>+{order.user.phone}</b>\n🕙Время заказа: {order.date.year}-{order.date.month}-{order.date.day}  {order.date.hour}:{order.date.minute}\n📍 Адрес: {order.address}\n\n"
                for order_detail in order_deails:
                    text += f"  {order_detail.product.name_ru}✖️{order_detail.count}\n"
                    summa += order_detail.product.price * order_detail.count
                text += f"\n<b>Общая сумма: </b>{summa} UZS"
            if lang == "uz":
                text = f"<b>🛒Buyurtmangiz</b>\n\n🆔 Buyurtma: <b>#{order.id}</b>\n"\
                f"👤 Xaridor: <b>+{order.user.phone}</b>\n🕙Buyurtma vaqti: {order.date.year}-{order.date.month}-{order.date.day}  {order.date.hour}:{order.date.minute}\n📍 Manzil: {order.address}\n\n"
                for order_detail in order_deails:
                    text += f"  {order_detail.product.name_uz}✖️{order_detail.count}\n"
                    summa += order_detail.product.price * order_detail.count
                text += f"<b>Jami: </b>{summa} UZS"
            if lang == "tr":
                text = f"<b>🛒Siparişiniz</b>\n\n🆔 Sipariş: <b>#{order.id}</b>\n"\
                f"👤 İstemci: <b>+{order.user.phone}</b>\n🕙Sipariş zamanı: {order.date.year}-{order.date.month}-{order.date.day}  {order.date.hour}:{order.date.minute}\n📍 Adres: {order.address}\n\n"
                for order_detail in order_deails:
                    text += f"  {order_detail.product.name_uz}✖️{order_detail.count}\n"
                    summa += order_detail.product.price * order_detail.count
                text += f"\n<b>Toplam miktar: </b>{summa} UZS"
            order.summa = summa
            order.save()
            await message.answer(text, reply_markup=markup)
            await state.set_state("confirm_order")
            
        # prices = []
        # if message.text == "🔵 Click":
        #     photo = 'https://click.uz/click/images/clickog.png'
        #     token = '398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065'
        # elif message.text == "🟢 Payme":
        #     photo = "https://cdn.paycom.uz/documentation_assets/payme_01.png"
        #     token = '371317599:TEST:1664877798422'
        # prices.append(
        #     types.LabeledPrice(label=f"Test uchun tanish", amount=int(1000) * 100))
        # await bot.send_invoice(chat_id=message.from_user.id, title=f'Test title',
        #                        description=f' Test description',
        #                        provider_token=token,
        #                        currency='UZS',
        #                        photo_url=photo,
        #                        photo_height=512,  # !=0/None or picture won't be shown
        #                        photo_width=512,
        #                        photo_size=512,
        #                        prices=prices,
        #                        start_parameter='hz-wto-tut',
        #                        payload="Payload"
        #                        )
        # await state.set_state("payment")        


@dp.message_handler(content_types=types.ContentType.LOCATION, state='get_address')
async def get_location_address(message: types.Message, state: FSMContext):
    location = message.location
    geolocator = Nominatim(user_agent="geoapiExercises")
    Latitude = str(location.latitude)
    Longitude = str(location.longitude)
    location = geolocator.geocode(Latitude + "," + Longitude)
    data = location.raw.get('display_name')
    data = data.split(',')
    name = f"{data[0]} {data[1]} {data[2]}"
    user = await get_user(message.from_user.id)
    lang = user.lang
    text = []
    if lang == 'uz':
        text = '🔰 Manzilni tasdiqlaysizmi?'
    elif lang == 'ru':
        text = '🔰 Вы подтверждаете адрес?'
    elif lang == 'tr':
        text = '🔰 Konumu onaylıyor musunuz?'
    await state.update_data(latitude=Latitude, longitude=Longitude, name=name,
                            display_name=location.raw.get('display_name'))
    await message.answer(text=location.raw.get('display_name'), reply_markup=ReplyKeyboardRemove())
    markup = await confirm_address(lang)
    await bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=markup)
    await state.set_state('confirm_address')


@dp.message_handler(content_types=types.ContentType.TEXT, state='get_address')
async def get_loc(message: types.Message, state: FSMContext):
    lang = await get_lang(message.from_id)
    if "⬅️" in  message.text:
            markup = await pay_method(lang)
            if lang == "uz":
                await message.answer("Iltimos to'lov usulini tanlang 👇", reply_markup=markup)
            elif lang == "ru":
                await message.answer("Пожалуйста, выберите способ оплаты 👇", reply_markup=markup)
            elif lang == "tr":
                await message.answer("Lütfen bir ödeme yöntemi seçin 👇", reply_markup=markup)
            await state.set_state("get_payment_method")
    elif message.text in ['🔂 Oldingi manzillar', '🔂 Предыдущие адреса', '🔂 Önceki adresler']:
        locations = await get_address(message.from_user.id)
        if locations:
            text = []
            if lang == 'uz':
                text = ['Kerakli mazilni tanlang', 'Manzillar']
            elif lang == 'ru':
                text = ['Выберите нужное место', 'Адреса']
            elif lang == 'tr':
                text = ['İstediğiniz mazili seçin', 'Adres listesi']
            markup = await location_keys(user_id=message.from_user.id, lang=lang)
            await message.answer(text=text[1], reply_markup=ReplyKeyboardRemove())
            await bot.send_message(text=text[0], chat_id=message.from_user.id, reply_markup=markup)
            await state.set_state('get_location')
        else:
            text = []
            if lang == 'uz':
                text = '🗑 Manzillar ro\'yxati bo\'sh'
            elif lang == 'ru':
                text = '🗑 Список адресов пустой'
            elif lang == 'tr':
                text = '🗑 Adres listesi boş'
            await message.answer(text)
    
@dp.message_handler(content_types=types.ContentType.TEXT, state='get_location')
async def get_loc(message: types.Message, state: FSMContext):
    lang = await get_lang(message.from_id)
    if "⬅️" in  message.text:
        lang = await get_lang(message.from_user.id)
        text = []
        if lang == 'uz':
            text = ['Yetkazish manzilini jo\'nating']
        elif lang == 'ru':
            text = ['Отправьте адрес доставки']
        elif lang == 'tr':
            text = ['Lütfen teslimat adresinizi gönderiniz']
        markup = await location_send(lang)
        await message.answer(text=f"{text[0]} 👇", reply_markup=markup)
        await state.set_state("get_address")
    else:
        loc = message.text
        location = await get_location_by_name(name=loc, user_id=message.from_id)
        if location is not None:
            geolocator = Nominatim(user_agent="geoapiExercises")
            Latitude = str(location.latitude)
            Longitude = str(location.longitude)
            location = geolocator.geocode(Latitude + "," + Longitude)
            data = location.raw.get('display_name')
            data = data.split(',')
            name = f"{data[0]} {data[1]} {data[2]}"
            user = await get_user(message.from_user.id)
            lang = user.lang
            text = []
            if lang == 'uz':
                text = '🔰 Manzilni tasdiqlaysizmi?'
            elif lang == 'ru':
                text = '🔰 Вы подтверждаете адрес?'
            elif lang == 'tr':
                text = '🔰 Konumu teyit ediyor musunuz?'
            await state.update_data(latitude=Latitude, longitude=Longitude, name=name,
                                    display_name=location.raw.get('display_name'))
            await message.answer(text=location.raw.get('display_name'), reply_markup=ReplyKeyboardRemove())
            markup = await confirm_address(lang)
            await bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=markup)
            await state.set_state('confirm_address')

@dp.message_handler(content_types=types.ContentType.TEXT, state='confirm_address')
async def get_loc(message: types.Message, state: FSMContext):
    lang = await get_lang(message.from_id)
    if "⬅️️" in message.text:
        markup = await pay_method(lang)
        if lang == "uz":
            await message.answer("Iltimos to'lov usulini tanlang 👇", reply_markup=markup)
        elif lang == "tr":
            await message.answer("Lütfen bir ödeme yöntemi seçin 👇", reply_markup=markup)
        elif lang == "ru":
            await message.answer("Пожалуйста, выберите способ оплаты 👇", reply_markup=markup)
        await state.set_state("get_payment_method")
    elif message.text in ["✅ Tasdiqlash", "✅ Подтвердить", "✅ Onayla"]:
        data = await state.get_data()
        latitude = data['latitude']
        longitude = data['longitude']
        loc_name = data['name']
        address = data['display_name']
        card_type = data["card_type"]
        date = datetime.datetime.now() + timedelta(hours=5)
        order = await add_order(user_id=message.from_id, date=date, address=address)
        await state.update_data(order_id=order.id)
        order.address = address
        carts = await get_cart_objects(message.from_id)
        for cart in carts:
            await add_order_detail(order_id=order.id, product_id=cart.product.id, count=cart.count)
        order_deails = await get_order_details(order.id) 
        summa = 0
        dish = 0
        counts = 0
        await add_address(latitude=latitude, longitude=longitude, user_id=message.from_user.id, name=loc_name)
        markup = await order_confirmation(lang)
        if lang == "uz":
            text = f"<b>🛒Sizning Buyurtmangiz</b>\n\n🆔 Buyurtma: <b>#{order.id}</b>\n"\
            f"👤 Xaridor: <b>+{order.user.phone}</b>\n🕙Buyurtma vaqti: {order.date.year}-{order.date.month}-{order.date.day}  {order.date.hour}:{order.date.minute}\n📍 Manzil: {order.address}\n\n"
            for order_detail in order_deails:
                text += f"{order_detail.product.name_uz}✖️{order_detail.count}\n"
                dish += order_detail.count * int(order_detail.product.dish)
                counts += order_detail.count
                summa += order_detail.product.price * order_detail.count
            text += f"<b>Jami: </b>{summa} UZS"
            text += f"\n<b>Bir martalik idish uchun to'lov: </b>{counts} \nJami: {dish} UZS"
            summa += dish
            text += f"\n<b>Umumiy summa: </b>{summa} UZS\n"
        elif lang == "ru":
            text = f"<b>🛒Ваш заказ</b>\n\n🆔 Заказ: <b>#{order.id}</b>\n"\
            f"👤 Заказчик: <b>+{order.user.phone}</b>\n🕙Время заказа: {order.date.year}-{order.date.month}-{order.date.day}  {order.date.hour}:{order.date.minute}\n📍 Адрес: {order.address}\n\n"
            for order_detail in order_deails:
                text += f"{order_detail.product.name_ru}✖️{order_detail.count}\n"
                summa += order_detail.product.price * order_detail.count
                dish += order_detail.count * int(order_detail.product.dish)
                counts += order_detail.count
            text += f"<b>Общий: </b>{summa} UZS\n"    
            text += f"\n<b>Плата за одноразовую посуду: </b>{counts} \nОбщий: {dish} UZS"
            summa += dish
            text += f"\n<b>Общая сумма: </b>{summa} UZS"
        elif lang == "tr":
            text = f"<b>🛒Siparişiniz</b>\n\n🆔 Sipariş: <b>#{order.id}</b>\n"\
            f"👤 İstemci: <b>+{order.user.phone}</b>\n🕙Sipariş zamanı: {order.date.year}-{order.date.month}-{order.date.day}  {order.date.hour}:{order.date.minute}\n📍 Adres: {order.address}\n\n"
            for order_detail in order_deails:
                text += f"  {order_detail.product.name_uz}✖️{order_detail.count}\n"
                summa += order_detail.product.price * order_detail.count
                dish += order_detail.count * int(order_detail.product.dish)
                counts += order_detail.count
            text += f"<b>Total: </b>{summa} UZS\n"
            text += f"\n<b>Tek konteyner ücreti: </b>{counts} \nTotal: {dish} UZS"
            summa += dish
            text += f"\n<b>Toplam miktar: </b>{summa} UZS"
        order.summa = summa
        order.pay_type = card_type
        order.save()
        await message.answer(text, reply_markup=markup)
        await state.set_state("confirm_order")
    elif message.text in ["🔄 Qayta jo\'natish", "🔄 Отправить повторно", "🔄 Tekrar gönderin"]:
        lang = await get_lang(message.from_user.id)
        text = []
        if lang == 'uz':
            text = ['Yetkazish manzilini jo\'nating']
        elif lang == 'ru':
            text = ['Отправьте адрес доставки']
        elif lang == 'tr':
            text = ['Lütfen teslimat adresinizi gönderiniz']
        markup = await location_send(lang)
        await message.answer(text=f"{text[0]} 👇", reply_markup=markup)
        await state.set_state("get_address")


@dp.message_handler(content_types=types.ContentType.TEXT, state='confirm_order')
async def get_loc(message: types.Message, state: FSMContext):
    lang = await get_lang(message.from_id)
    data = await state.get_data()
    order_id = data['order_id']
    order = await get_order(order_id)
    if message.text in ["❌ Bekor qilish", "❌ İptal", "❌ Отмена"]:
        await clear_cart(message.from_id)
        order.delete()
        markup = await user_menu(lang)
        if lang == "uz":
            await message.answer("🗑 Savatcha tozalandi. Iltimos kerakli bo'limni tanlang 👇", reply_markup=markup)
        elif lang == "ru":
            await message.answer("🗑 Корзина очищена. Выберите нужный раздел👇", reply_markup=markup)
        elif lang == "tr":
            await message.answer("🗑 Sepet temizlendi. Lütfen istediğiniz bölümü seçin 👇", reply_markup=markup)
        await state.set_state("get_command")
    elif message.text in ["✅ Подтвердить заказ", "✅ Buyurtmani tasdiqlash", "✅ Sipariş onaylamak"]:
        markup = await comment_keyboard(lang)
        if lang == "uz":
            await message.answer("Buyurtma uchun qoshimcha izohlar qo'shishni istaysizmi 👇", reply_markup=markup)
        elif lang == "tr":
            await message.answer("Sipariş için ek yorum eklemek ister misiniz 👇", reply_markup=markup)
        elif lang == "ru":
            await message.answer("Хотите добавить дополнительные комментарии к заказу 👇", reply_markup=markup)
        await state.set_state("comment")
        

@dp.message_handler(content_types=types.ContentType.TEXT, state='comment')
async def get_loc(message: types.Message, state: FSMContext):
    lang = await get_lang(message.from_id)
    data = await state.get_data()
    order_id = data['order_id']
    order = await get_order(order_id)
    order_details = await get_order_details(order_id)
    if message.text in ["➡️ Tashlab ketish", "➡️ Пропустить", "➡️ Atlamak"]:
        order.comment = "Izohsiz"
        order.save()
        if order.service_type != "pick":
            prices = []
            card_type = data["card_type"]
            counts = 0
            if card_type != "cash":
                text = ''
                dish = 0
                for order_detail in order_details:
                    dish += order_detail.count * int(order_detail.product.dish)
                    counts += order_detail.count
                    if lang == "uz":                        
                        text = "To'lovni amalga oshiring 👇"
                        prices.append(
                            types.LabeledPrice(label=f"{order_detail.product.name_uz} ✖️ {order_detail.count}", amount=int(order_detail.product.price) * int(order_detail.count) * 100))
                    elif lang == "ru":
                        text = "Оплатите 👇"
                        prices.append(
                            types.LabeledPrice(label=f"{order_detail.product.name_ru} ✖️ {order_detail.count}", amount=int(order_detail.product.price) * int(order_detail.count) * 100))
                    elif lang == "tr":
                        text = "Ödemeyi yap 👇"
                        prices.append(
                            types.LabeledPrice(label=f"{order_detail.product.name_tr} ✖️ {order_detail.count}", amount=int(order_detail.product.price) * int(order_detail.count) * 100))
                if counts != 0:    
                    if lang == "uz":
                        prices.append(
                            types.LabeledPrice(label=f"Bir martalik idish uchun to'lov", amount=dish * 100))
                    if lang == "ru":
                        prices.append(
                            types.LabeledPrice(label=f"Плата за одноразовую посуду", amount=dish * 100))
                    if lang == "tr":
                        prices.append(
                            types.LabeledPrice(label=f"Tek konteyner ücreti", amount=dish * 100))
                    
                photo = 'https://click.uz/click/images/clickog.png'
                keys = await back_keyboard(lang)
                await message.answer(text=text, reply_markup=keys)
                message_id = int(message.message_id) + 1
                await state.update_data(message_id=message_id)
                token = '333605228:LIVE:12098_B4831627769C70BA818FCFBF94A8FB7A6EDBB452'
                # token = "398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065"
                await bot.send_invoice(chat_id=message.from_user.id, title=f'Mustafa Turkish Cusine',
                                    description=f'Mustafa Turkish',
                                    provider_token=token,
                                    currency='UZS',
                                    photo_url=photo,
                                    photo_height=512,  # !=0/None or picture won't be shown
                                    photo_width=512,
                                    photo_size=512,
                                    prices=prices,
                                    start_parameter='hz-wto-tut',
                                    payload="Payload"
                                    )
                await state.set_state("payment") 
            else:   
                await clear_cart(message.from_id)
                summa = 0
                dish = 0
                counts = 0
                text = f"<b>🛒Yangi buyurtma</b>\n\n🆔 Buyurtma: <b>#{order.id}</b>\n"\
                f"👤 Xaridor: <b>+{order.user.phone}</b>\n🕙Buyurtma vaqti: {order.date.year}-{order.date.month}-{order.date.day}  {order.date.hour}:{order.date.minute}\n📍 Manzil: {order.address}\n\n"
                for order_detail in order_details:
                    dish += order_detail.count * int(order_detail.product.dish)
                    counts += order_detail.count
                    text += f"{order_detail.product.name_uz}✖️{order_detail.count}\n"
                    summa += order_detail.product.price * order_detail.count
                text += f"<b>Jami: </b>{summa} UZS"
                text += f"\n<b>Bir martalik idish uchun to'lov: </b>{counts} Jami: {dish} UZS"
                summa += dish
                text += f"\n<b>Umumiy summa: </b>{summa} UZS\n"
                text += f"\n<b>To'lov: </b> 💴 Naqd pul orqali"
                order.status = 'confirmed'
                order.save()
                await bot.send_message(chat_id=config.GROUPS_ID, text=text)
                await clear_cart(message.from_user.id)
                user = await get_user(message.from_user.id)
                await create_order(user, order_id, data['longitude'], data['latitude'], data['display_name'])
                markup = await user_menu(lang)
                if lang == "uz":
                    await message.answer("✔️ Buyurtma muvaffaqiyatli amalga oshirildi. Iltimos kerakli bo'limni tanlang 👇", reply_markup=markup)
                elif lang == "tr":
                    await message.answer("✔️ Sipariş başarıyla verildi. Lütfen istediğiniz bölümü seçin 👇", reply_markup=markup)
                elif lang == "ru":
                    await message.answer("✔️ Заказ был успешно размещен. Пожалуйста, выберите нужный раздел 👇", reply_markup=markup)
                await state.set_state("get_command")
        if order.service_type == "pick":
            order.status = "confirmed"
            order.save()
            summa = 0
            dish = 0
            counts = 0
            text = f"<b>🛒Yangi buyurtma</b>\n\n🆔 Buyurtma: <b>#{order.id}</b>\n"\
            f"👤 Xaridor: <b>+{order.user.phone}</b>\n🕙Buyurtma vaqti: {order.date.year}-{order.date.month}-{order.date.day}  {order.date.hour}:{order.date.minute}\n📍 Manzil: {order.address}\n\n"
            for order_detail in order_details:
                text += f"{order_detail.product.name_uz}✖️{order_detail.count}\n"
                summa += order_detail.product.price * order_detail.count
                dish += order_detail.count * int(order_detail.product.dish)
                counts += order_detail.count
            text += f"<b>Jami: </b>{summa} UZS"
            text += f"\n<b>Bir martalik idish uchun to'lov: </b>{counts} \nJami: {dish} UZS"
            summa += dish
            text += f"\n<b>Umumiy summa: </b>{summa} UZS\n"
            text += f"\n<b>To'lov: </b> Olib ketish"
            text += f"\n\n<b>Izoh: </b> {order.comment}"
            await bot.send_message(chat_id=config.GROUPS_ID, text=text)
            markup = await user_menu(lang)
            await clear_cart(message.from_user.id)
            if lang == "uz":
                await message.answer("✔️ Buyurtma muvaffaqiyatli amalga oshirildi. Buyurtmani quyidagi manzildan olib ketishingiz mumkin 👇\nOybek ko'chasi 44, orientir: 'Avalon' biznes markazi", reply_markup=markup)
            elif lang == "tr":
                await message.answer("✔️ Sipariş başarıyla verildi. Aşağıdaki adresten siparişinizi teslim alabilirsiniz 👇\nAibek caddesi 44, dönüm noktası: İş merkezi 'Avalon'", reply_markup=markup)
            elif lang == "ru":
                await message.answer("✔️ Заказ был успешно размещен.Вы можете забрать заказ по адресу 👇\nУлица айбека 44, ориентир: Бизнес центр 'Avalon'", reply_markup=markup)
            await state.set_state("get_command")
    if message.text in ["💬 Izoh qo'shish", "💬 Добавить комментарий", "💬 Yorum ekle"]:
        if lang == "uz":
            await message.answer("Izohingizni kirting 👇", reply_markup=ReplyKeyboardRemove())
        elif lang == "tr":
            await message.answer("Yorumunuzu girin 👇", reply_markup=ReplyKeyboardRemove())
        elif lang == "ru":
            await message.answer("Оставьте свой комментарий 👇", reply_markup=ReplyKeyboardRemove())
        await state.set_state("get_comment")
    if message.text in ["⬅️️ Orqaga", "⬅️️ Назад", "⬅️️ Geri"]:
        markup = await order_type(lang)
        if lang == "uz":
            await message.answer(text="Xizmat turini tanlang", reply_markup=markup)
        elif lang == "tr":
            await message.answer(text="Hizmet türünü seçin", reply_markup=markup)
        elif lang == "ru":
            await message.answer(text="Выберите тип услуги", reply_markup=markup)
        
 
@dp.message_handler(content_types=types.ContentType.TEXT, state='get_comment')
async def get_loc(message: types.Message, state: FSMContext):
    lang = await get_lang(message.from_id)
    data = await state.get_data()
    order_id = data['order_id']
    order = await get_order(order_id)
    order_details = await get_order_details(order_id)
    order.comment = message.text
    order.save()
    if order.service_type != "pick":
        prices = []
        card_type = data["card_type"]
        counts = 0
        if card_type != "cash":
            text = ''
            dish = 0
            for order_detail in order_details:
                dish += order_detail.count * int(order_detail.product.dish)
                counts+= order_detail.count
                if lang == "uz":                        
                    text = "To'lovni amalga oshiring 👇"
                    prices.append(
                        types.LabeledPrice(label=f"{order_detail.product.name_uz} ✖️ {order_detail.count}", amount=int(order_detail.product.price) * int(order_detail.count) * 100))
                elif lang == "ru":
                    text = "Оплатите 👇"
                    prices.append(
                        types.LabeledPrice(label=f"{order_detail.product.name_ru} ✖️ {order_detail.count}", amount=int(order_detail.product.price) * int(order_detail.count) * 100))
                elif lang == "tr":
                    text = "Ödemeyi yap 👇"
                    prices.append(
                        types.LabeledPrice(label=f"{order_detail.product.name_tr} ✖️ {order_detail.count}", amount=int(order_detail.product.price) * int(order_detail.count) * 100))
            if lang == "uz":
                prices.append(
                    types.LabeledPrice(label=f"Bir martalik idish uchun to'lov", amount=dish * 100))
            if lang == "ru":
                prices.append(
                    types.LabeledPrice(label=f"Плата за одноразовую посуду", amount=dish * 100))
            if lang == "tr":
                prices.append(
                    types.LabeledPrice(label=f"Tek konteyner ücreti", amount=dish * 100))
                
            photo = 'https://click.uz/click/images/clickog.png'
            keys = await back_keyboard(lang)
            await message.answer(text=text, reply_markup=keys)
            message_id = int(message.message_id) + 1
            await state.update_data(message_id=message_id)
            token = '333605228:LIVE:12098_B4831627769C70BA818FCFBF94A8FB7A6EDBB452'
            # token = "398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065"
            await bot.send_invoice(chat_id=message.from_user.id, title=f'Mustafa Turkish Cusine',
                                description=f'Mustafa Turkish',
                                provider_token=token,
                                currency='UZS',
                                photo_url=photo,
                                photo_height=512,  # !=0/None or picture won't be shown
                                photo_width=512,
                                photo_size=512,
                                prices=prices,
                                start_parameter='hz-wto-tut',
                                payload="Payload"
                                )
            await state.set_state("payment") 
        else:   
            await clear_cart(message.from_id)
            summa = 0
            dish = 0
            counts = 0
            text = f"<b>🛒Yangi buyurtma</b>\n\n🆔 Buyurtma: <b>#{order.id}</b>\n"\
            f"👤 Xaridor: <b>+{order.user.phone}</b>\n🕙Buyurtma vaqti: {order.date.year}-{order.date.month}-{order.date.day}  {order.date.hour}:{order.date.minute}\n📍 Manzil: {order.address}\n\n"
            for order_detail in order_details:
                dish += order_detail.count * int(order_detail.product.dish)
                counts += order_detail.count
                text += f"{order_detail.product.name_uz}✖️{order_detail.count}\n"
                summa += order_detail.product.price * order_detail.count
            text += f"<b>Jami: </b>{summa} UZS"
            text += f"\n<b>Bir martalik idish uchun to'lov: </b>{counts} \nJami: {dish} UZS"
            summa += dish
            text += f"\n<b>Umumiy summa: </b>{summa} UZS\n"
            text += f"\n<b>To'lov: </b> 💴 Naqd pul orqali"
            text += f"\n\n<b>Izoh: </b> {order.comment}"
            order.status = 'confirmed'
            order.save()
            await bot.send_message(chat_id=config.GROUPS_ID, text=text)
            await clear_cart(message.from_user.id)
            markup = await user_menu(lang)
            if lang == "uz":
                await message.answer("✔️ Buyurtma muvaffaqiyatli amalga oshirildi. Iltimos kerakli bo'limni tanlang 👇", reply_markup=markup)
            elif lang == "tr":
                await message.answer("✔️ Sipariş başarıyla verildi. Lütfen istediğiniz bölümü seçin 👇", reply_markup=markup)
            elif lang == "ru":
                await message.answer("✔️ Заказ был успешно размещен. Пожалуйста, выберите нужный раздел 👇", reply_markup=markup)
            await state.set_state("get_command")
    if order.service_type == "pick":
        order.status = "confirmed"
        order.save()
        summa = 0
        dish = 0
        counts = 0
        text = f"<b>🛒Yangi buyurtma</b>\n\n🆔 Buyurtma: <b>#{order.id}</b>\n"\
        f"👤 Xaridor: <b>+{order.user.phone}</b>\n🕙Buyurtma vaqti: {order.date.year}-{order.date.month}-{order.date.day}  {order.date.hour}:{order.date.minute}\n📍 Manzil: {order.address}\n\n"
        for order_detail in order_details:
            text += f"{order_detail.product.name_uz}✖️{order_detail.count}\n"
            summa += order_detail.product.price * order_detail.count
            dish += order_detail.count * int(order_detail.product.dish)
            counts += order_detail.count
        text += f"<b>Jami: </b>{summa} UZS"
        text += f"\n<b>Bir martalik idish uchun to'lov: </b>{counts} \nJami: {dish} UZS"
        summa += dish
        text += f"\n<b>Umumiy summa: </b>{summa} UZS\n"
        text += f"\n<b>To'lov: </b> Olib ketish"
        text += f"\n\n<b>Izoh: </b> {order.comment}"
        await bot.send_message(chat_id=config.GROUPS_ID, text=text)
        markup = await user_menu(lang)
        await clear_cart(message.from_user.id)
        if lang == "uz":
            await message.answer("✔️ Buyurtma muvaffaqiyatli amalga oshirildi. Buyurtmani quyidagi manzildan olib ketishingiz mumkin 👇\nOybek ko'chasi 44, orientir: 'Avalon' biznes markazi", reply_markup=markup)
        elif lang == "tr":
            await message.answer("✔️ Sipariş başarıyla verildi. Aşağıdaki adresten siparişinizi teslim alabilirsiniz 👇\nAibek caddesi 44, dönüm noktası: İş merkezi 'Avalon'", reply_markup=markup)
        elif lang == "ru":
            await message.answer("✔️ Заказ был успешно размещен.Вы можете забрать заказ по адресу 👇\nУлица айбека 44, ориентир: Бизнес центр 'Avalon'", reply_markup=markup)
        await state.set_state("get_command")
                         

@dp.pre_checkout_query_handler(lambda query: True, state='payment')
async def checkout(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=types.ContentTypes.SUCCESSFUL_PAYMENT, state="payment")
async def got_payment(message: types.Message, state: FSMContext):
    lang = await get_lang(message.from_id)
    data = await state.get_data()
    order_id = data['order_id']
    order = await get_order(order_id)
    order.status = "PAID"
    order.save()    
    message_id = int(data["message_id"])
    await bot.delete_message(chat_id=message.from_user.id, message_id=message_id)
    message_id = int(data["message_id"]) + 1 
    await bot.delete_message(chat_id=message.from_user.id, message_id=message_id)
    order_details = await get_order_details(order_id)
    await bot.delete_message(chat_id=message.from_user.id, message_id=message_id)
    await clear_cart(message.from_id)
    summa = 0
    dish = 0
    counts = 0
    text = f"<b>🛒Yangi buyurtma</b>\n\n🆔 Buyurtma: <b>#{order.id}</b>\n"\
    f"👤 Xaridor: <b>+{order.user.phone}</b>\n🕙Buyurtma vaqti: {order.date.year}-{order.date.month}-{order.date.day}  {order.date.hour}:{order.date.minute}\n📍 Manzil: {order.address}\n\n"
    for order_detail in order_details:
        dish += order_detail.count * int(order_detail.product.dish)
        counts += order_detail.count
        text += f"{order_detail.product.name_uz}✖️{order_detail.count}\n"
        summa += order_detail.product.price * order_detail.count
    text += f"<b>Jami: </b>{summa} UZS"
    text += f"\n<b>Bir martalik idish uchun to'lov: </b>{counts} \nJami: {dish} UZS"
    summa += dish
    text += f"\n<b>Umumiy summa: </b>{summa} UZS\n"
    text += f"\n<b>To'lov: </b> ✅ TO'LANDI"
    text += f"\n\n<b>Izoh: </b> {order.comment}"
    await bot.send_message(chat_id=config.GROUPS_ID, text=text)
    markup = await user_menu(lang)
    if lang == "uz":
        await message.answer("✔️ Buyurtma muvaffaqiyatli amalga oshirildi. Iltimos kerakli bo'limni tanlang 👇", reply_markup=markup)
    elif lang == "tr":
        await message.answer("✔️ Sipariş başarıyla verildi. Lütfen istediğiniz bölümü seçin 👇", reply_markup=markup)
    elif lang == "ru":
        await message.answer("✔️ Заказ был успешно размещен. Пожалуйста, выберите нужный раздел 👇", reply_markup=markup)
    await state.set_state("get_command")


@dp.message_handler(content_types=types.ContentTypes.TEXT, state="payment")
async def get_payment_back(message: types.Message, state: FSMContext):
    if "⬅️" in message.text:
        lang = await get_lang(message.from_id)
        data = await state.get_data()
        message_id = int(data["message_id"])
        await bot.delete_message(chat_id=message.from_user.id, message_id=message_id)
        message_id = int(data["message_id"]) + 1 
        await bot.delete_message(chat_id=message.from_user.id, message_id=message_id)
        order_id = data['order_id']
        order = await get_order(order_id)
        order.delete()
        text = await get_carts(message.from_id)
        if text is not None:
            cart_test = await check_cart(message.from_id)
            if cart_test:
                markup = await cart_keyboard(lang=lang, user_id=message.from_id)
                await message.answer(text=text, reply_markup=markup, parse_mode='HTML')
            else:
                go_m = await go_order(lang)
                markup = await back_keyboard(lang)
                if lang == "uz":
                    await message.answer(text, reply_markup=markup)
                    await message.answer("Xaridni boshlang ", reply_markup=go_m)
                elif lang == "tr":
                    await message.answer(text, reply_markup=markup)
                    await message.answer("Alışverişe başla", reply_markup=go_m)
                elif lang == "ru":
                    await message.answer(text, reply_markup=markup)
                    await message.answer("Начать покупки", reply_markup=go_m)
        await state.set_state("get_cart_command")
    else:
        pass
