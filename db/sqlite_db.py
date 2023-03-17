import sqlite3
from create_bot import bot, payment_token
import time
from aiogram import types

def sql_start():
    global connect, cursor
    connect = sqlite3.connect("pizza_bot_db.db")
    cursor = connect.cursor()
    if connect:
        print("Database connected")
    cursor.execute("""CREATE TABLE IF NOT EXISTS menu (
        img TEXT,
        name TEXT PRIMARY KEY,
        desc TEXT,
        price INT
        )""")
    connect.commit()
    
async def sql_add(state):
    async with state.proxy() as data:
        print(tuple(data.values()))
        cursor.execute("INSERT INTO menu VALUES (?, ?, ?, ?)", tuple(data.values()))
    connect.commit()
    
async def sql_read2():
    return cursor.execute("SELECT * FROM menu").fetchall()
    
    
async def sql_read(message):
    for data in cursor.execute("SELECT * FROM menu").fetchall():
        url = data[0].split("$")[0]
        price = int(data[3]) * 100
        lblPrice = types.LabeledPrice(label=f"{data[1]}", amount=price)
        await bot.send_invoice(
            message.from_user.id,
            title = f"*{data[1]}*",
            description = f"{data[2]}",
            provider_token=payment_token,
            currency="rub",
            photo_url = f"{url}",
            photo_height=512,
            photo_width=800,
            photo_size=512,
            is_flexible=False,
            prices=[lblPrice],
            need_email=True,
            need_phone_number=True,
            need_shipping_address=True,
            start_parameter="pizza",
            payload=f"Клиент заказал: {data[1]}"
        )
        #data[0], f"Название: {data[1]}\nОписание: {data[2]}\nЦена: {data[3]}")
        if data != cursor.execute("SELECT * FROM menu").fetchall()[-1]:
            time.sleep(3)
    
    if payment_token.split(":")[1] == "TEST":
        await bot.send_message(message.from_user.id, "*ВНИМАНИЕ*\nПодключен тестовый платеж. Чтобы оплатить покупку, воспользуйтесь реквизитами: `1111 1111 1111 1026, 12/22, CVC 000`")
        
        
async def delete_item(data):
    cursor.execute("DELETE FROM menu WHERE name == ?", (data,))
    connect.commit()