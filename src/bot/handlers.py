from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

directions_list = [
    'Логопедия',
    'Логопедия',
    'Логопедия',
    'Логопедия',
]


def directions_kb():
    kb = InlineKeyboardBuilder()
    buttons = [
        InlineKeyboardButton(text=str(btn), callback_data=f'_direction_{pk}')
        for pk, btn in enumerate(directions_list)
    ]
    kb.add(
        *buttons
    )
    return kb.as_markup()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer('Hello!')


@router.message(Command('directions'))
async def directions(message: Message):
    await message.answer('Направления', reply_markup=directions_kb())


