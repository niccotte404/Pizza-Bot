from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

addBtn = KeyboardButton("/Загрузить")
delBtn = KeyboardButton("/Удалить")

rkm_admin = ReplyKeyboardMarkup(resize_keyboard=True)

rkm_admin.row(addBtn, delBtn)