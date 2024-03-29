from aiogram.types import InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.db.crud import DirectionCrud

from src.bot.utils import load_resources

resource = load_resources()


async def directions():
    direction_objects = await DirectionCrud().all()

    builder = InlineKeyboardBuilder()

    for obj in direction_objects:
        builder.add(
            InlineKeyboardButton(text=obj.title, callback_data=f'direction__{obj.id}')
        )

    builder.adjust(3)

    return builder.as_markup()


main_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text=resource.keyboards.get('directions')),
         KeyboardButton(text=resource.keyboards.get('sign_up'))],
        [KeyboardButton(text=resource.keyboards.get('support'))]
    ]
)
