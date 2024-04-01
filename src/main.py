from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
import asyncio
import logging

from bot import main_router

from bot.settings import BotConfig
from src.bot.commands import Commands


async def bot_start(bot: Bot) -> None:
    """ функция срабатывает при запуске бота """
    await Commands.set_commands(bot)


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=BotConfig.TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    dp.startup.register(bot_start)

    dp.include_routers(main_router, )

    await bot.delete_webhook(drop_pending_updates=True)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
