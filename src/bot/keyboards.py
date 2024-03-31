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

    builder.adjust(1)

    return builder.as_markup()


def sig_up_keyboard_builder(objects: list, field: str):
    builder = InlineKeyboardBuilder()
    if field == 'date':
        dates = set([obj.date for obj in objects])
        for date in dates:
            builder.add(
                InlineKeyboardButton(
                    text=date.strftime("%d.%m.%Y"),
                    callback_data=f'{field}__{date.strftime("%Y-%m-%d")}')
            )
    elif field == 'time':
        print(objects)
        for obj in objects:
            builder.add(
                InlineKeyboardButton(text=obj.time.strftime("%H:%M"), callback_data=f'{field}__{obj.id}')
            )

    builder.adjust(4)
    return builder.as_markup()


main_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text=resource.keyboards.get('directions')),
         KeyboardButton(text=resource.keyboards.get('sign_up'))],
        [KeyboardButton(text=resource.keyboards.get('support'))]
    ]
)

cancel_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text=resource.keyboards.get('cancel')), ]
    ]
)
