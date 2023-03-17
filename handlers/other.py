from aiogram import types, Dispatcher
import string, json

async def forbidden_words_delete(message: types.Message):
    if {i.lower().translate(str.maketrans("", "", string.punctuation)) for i in message.text.split(" ")}\
        .intersection(set(json.load(open("stopwords.json")))) != set():
        await message.reply("Маты запрещены")
        await message.delete()
        

def register_handler_other(dp: Dispatcher):
    dp.register_message_handler(forbidden_words_delete)