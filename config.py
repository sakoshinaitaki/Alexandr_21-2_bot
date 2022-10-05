from aiogram import Bot, Dispatcher
from decouple import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage
TOKEN = config("TOKEN")

storage = MemoryStorage()
ADMINS = [5055927981]
bot = Bot(TOKEN)
dp = Dispatcher(bot=bot, storage=storage)