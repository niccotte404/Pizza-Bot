from aiogram.utils import executor
from create_bot import dp
from handlers import client, admin, other
from db import sqlite_db


async def on_startup(_):
    print("Bot started")
    sqlite_db.sql_start()

    
client.register_handler_client(dp)
admin.register_handler_admin(dp)
other.register_handler_other(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)



# @dp.message_handler(lambda message: "что-либо" in message.text) возвращает True если ч.л. в message
# @dp.message_handler(lambda message: message.text.startswith("что-либо")) ну понятно