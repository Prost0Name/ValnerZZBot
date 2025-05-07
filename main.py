import asyncio
from bot import get_bot, get_dispatcher
from model import init_db, close_db

async def main():
    await init_db()
    bot = get_bot()
    dp = get_dispatcher()
    try:
        await dp.start_polling(bot)
    finally:
        await close_db()

if __name__ == "__main__":
    asyncio.run(main()) 