from aiogram.types import Message
from src.bot.db.crud import UserCrud
from aiogram.fsm.state import StatesGroup, State


async def get_or_create_user(message: Message):
    user = await UserCrud().get(message.from_user.id)
    if user:
        return user, False
    else:
        user = await UserCrud().create(
            name=message.from_user.first_name,
            tg_id=message.from_user.id,
        )
        return user, True
