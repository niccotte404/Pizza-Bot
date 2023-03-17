from aiogram import types, Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text

answ = dict()

bot = Bot(token="5004997382:AAF28eNkXgaLY-lLqUFFxeWN5DmqGieeceQ")
dp = Dispatcher(bot)

ikm = InlineKeyboardMarkup(row_width=1)
likeBtn = InlineKeyboardButton(text="Like", callback_data="like_1")
dislikeBtn = InlineKeyboardButton(text="Dislike", callback_data="like_-1")
ikm.add(likeBtn, dislikeBtn)

@dp.message_handler(commands=["test"])
async def start_inline_callback_btn(message: types.Message):
    await message.answer("Голосование", reply_markup=ikm)
    
@dp.callback_query_handler(Text(startswith="like_"))
async def callback_func_for_www(callback: types.CallbackQuery):
    
    res = int(callback.data.split("_")[1])
    if f"{callback.from_user.id}" not in answ:
        answ[f"{callback.from_user.id}"] = res
        await callback.answer("Вы проголосовали")
    else:
        await callback.answer("Вы уже проголосовали", show_alert=True)
    
    # await callback.message.answer("Вы нажали кнопку") Отправка в сообщении
    # await callback.answer("Вы нажали кнопку") Всплывающее окно
    # await callback.answer("Вы нажали кнопку", show_alert=True) Всплывающее окно с подтверждением

executor.start_polling(dp, skip_updates=True)