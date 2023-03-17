from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
import asyncio
from aiogram.contrib.fsm_storage.memory import MemoryStorage

payment_token = ""
storage = MemoryStorage()

loop = asyncio.get_event_loop()

bot = Bot(token="", parse_mode=types.ParseMode.MARKDOWN)
dp = Dispatcher(bot, storage=storage, loop=loop)