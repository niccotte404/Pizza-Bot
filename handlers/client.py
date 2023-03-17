from aiogram import types, Dispatcher
from aiogram.utils.exceptions import CantInitiateConversation, BotBlocked
from create_bot import bot
from keyboards.client_kb import rkm_client
from aiogram.types import ReplyKeyboardRemove
from db import sqlite_db
from create_bot import dp
from aiogram.types.message import ContentType

async def info(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, "Добро пожаловать в нашу пиццерию))", reply_markup=rkm_client)
    except (CantInitiateConversation, BotBlocked):
        await message.reply("Общение с ботом через ЛС, напишите ему:\n @del1c1ous_pizza_bot")


async def time_table(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, "Пн-Пт: 8.00-23.00, Сб-Вс: 9.00-21.00")
    except (CantInitiateConversation, BotBlocked):
        await message.reply("Общение с ботом через ЛС, напишите ему:\n @del1c1ous_pizza_bot")


async def location(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, "г. Сосиска, ул. Колбасная, д. 15")
    except (CantInitiateConversation, BotBlocked):
        await message.reply("Общение с ботом через ЛС, напишите ему:\n @del1c1ous_pizza_bot")
        
        
async def menu(message: types.Message):
    await sqlite_db.sql_read(message)
    
    
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
        
        
        
async def process_successful_payment(message: types.Message):
    print('successful_payment:')
    pmnt = message.successful_payment.to_python()
    for key, val in pmnt.items():
        print(f'{key} = {val}')

    await bot.send_message(message.chat.id, "*Вы успешно приобрели пиццу*\nКурьер прибудет с минуы на минуту. Приятного аппетита!")
    
        
        
def register_handler_client(dp: Dispatcher):
    dp.register_message_handler(info, commands=["start", "help"])
    dp.register_message_handler(time_table, commands=["Расписание"])
    dp.register_message_handler(location, commands=["Расположение"])
    dp.register_message_handler(menu, commands=["Меню"])
    dp.register_pre_checkout_query_handler(process_pre_checkout_query, lambda query: True)
    dp.register_message_handler(process_successful_payment, content_types=ContentType.SUCCESSFUL_PAYMENT)