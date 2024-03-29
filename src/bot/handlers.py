from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, InputFile, FSInputFile

from src.bot import resources
from src.bot import keyboards as kb

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(resources.texts.get('start'))


@router.message(Command('directions'))
async def directions(message: Message):
    await message.answer_photo(
        FSInputFile(resources.images.get('directions')),
        reply_markup=await kb.directions()
    )
