from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.db.crud import DirectionCrud


async def directions():
    direction_objects = await DirectionCrud().all()

    builder = InlineKeyboardBuilder()

    for obj in direction_objects:
        builder.add(
            InlineKeyboardButton(text=obj.title, callback_data=f'direction__{obj.id}')
        )

    builder.adjust(3)

    return builder.as_markup()