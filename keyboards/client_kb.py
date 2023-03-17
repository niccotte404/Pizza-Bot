from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

timetableBtn = KeyboardButton("/Расписание")
locationBtn = KeyboardButton("/Расположение")
menuBtn = KeyboardButton("/Меню")
# shareContactsBtn = KeyboardButton("Поделиться контактом", request_contact=True)
# shareLocationBtn = KeyboardButton("Отправить местоположение", request_location=True)

rkm_client = ReplyKeyboardMarkup(resize_keyboard=True)

rkm_client.add(timetableBtn).add(locationBtn).insert(menuBtn)
# rkm_client.add(timetableBtn).add(locationBtn).add(menuBtn)    Добавляет каждую кнопку в новую строку
# rkm_client.row(timetableBtn, locationBtn, menuBtn) Добавляет все кнопки в одну строку


# rkm_client.add(shareContactsBtn).add(shareLocationBtn)