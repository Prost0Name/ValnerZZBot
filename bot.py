from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from config import API_TOKEN
from handlers import register_routers

def get_bot():
    return Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

def get_dispatcher():
    dp = Dispatcher()
    register_routers(dp)
    return dp 