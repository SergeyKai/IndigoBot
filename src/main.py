from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
import asyncio
import logging

from bot import main_router

from bot.settings import BotConfig


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=BotConfig.TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    await bot.delete_webhook(drop_pending_updates=True)

    dp.include_routers(main_router, )

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
