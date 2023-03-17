from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from create_bot import bot
from db.sqlite_db import sql_add, sql_read2, delete_item
from keyboards import admin_kb
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

ID = None

class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()
    
    
async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, "Чо надо?", reply_markup=admin_kb.rkm_admin)
    await message.delete()
    
    
async def cm_start(message: types.Message):
    
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.reply("Загрузи фото, в поле CAPTION укажите URL на фото")
        
        
        
async def cansel_handler(message: types.Message, state: FSMContext):
    
    if message.from_user.id == ID:
        curr_state = state.get_state()
        if curr_state == None:
            return
        await state.finish()
        await message.reply("OK")
    
    
    
async def load_photo(message: types.Message, state: FSMContext):
    
    if message.from_user.id == ID:
        try:
            async with state.proxy() as data:
                data["photo"] = message.caption + "$" + message.photo[0].file_id
            await FSMAdmin.next()
            await message.reply("Теперь введите название")
        except TypeError:
            await message.reply("Вы не отправили URL в поле CAPTION", reply_markup=admin_kb.rkm_admin)
            state.finish()
            
    
    
    
async def set_name(message: types.Message, state: FSMContext):
    
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data["name"] = message.text
        await FSMAdmin.next()
        await message.reply("Введите описание")
    


async def set_description(message: types.Message, state: FSMContext):
    
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data["description"] = message.text
        await FSMAdmin.next()
        await message.reply("Теперь укажите цену")
    
    
    
async def set_price(message: types.Message, state: FSMContext):

    if message.from_user.id == ID:
        async with state.proxy() as data:
            data["price"] = int(message.text)

        await sql_add(state)
        await state.finish()
        
        
async def del_callback(callback: types.CallbackQuery):
    nm = callback.data.replace("del ", "")
    await delete_item(nm)
    await callback.answer(text=f"{nm} удалена", show_alert=True)

    
async def del_item(message: types.Message):
    if message.from_user.id == ID:
        read = await sql_read2()
        for item in read:
            await bot.send_photo(message.from_user.id, item[0].split("$")[1], f"Название: {item[1]}\nОписание: {item[2]}\nЦена: {item[3]}")
            ikm = InlineKeyboardMarkup()
            delBtn = InlineKeyboardButton(text=f"Удалить {item[1]}", callback_data=f"del {item[1]}")
            ikm.add(delBtn)
            await bot.send_message(message.from_user.id, text="^^^", reply_markup=ikm)
    

    
def register_handler_admin(dp: Dispatcher):
    dp.register_message_handler(make_changes_command, commands=["moderator"], is_chat_admin=True)
    dp.register_message_handler(cm_start, commands=["Загрузить"], state=None)
    dp.register_message_handler(cansel_handler, Text(equals="отмена", ignore_case=True), state="*")
    dp.register_message_handler(cansel_handler, state="*", commands=["отмена"])
    dp.register_message_handler(load_photo, content_types=["photo"], state=FSMAdmin.photo)
    dp.register_message_handler(set_name, state=FSMAdmin.name)
    dp.register_message_handler(set_description, state=FSMAdmin.description)
    dp.register_message_handler(set_price, state=FSMAdmin.price)
    dp.register_callback_query_handler(del_callback, lambda x: x.data and x.data.startswith("del "))
    dp.register_message_handler(del_item, commands=["Удалить"])
