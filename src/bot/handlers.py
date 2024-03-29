from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, FSInputFile

from src.bot import keyboards as kb
from src.bot.utils import load_resources

resource = load_resources()

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(resource.texts.get('start'), reply_markup=kb.main_keyboard)


@router.message(F.text == resource.keyboards.get('directions'))
@router.message(Command('directions'))
async def directions(message: Message):
    await message.answer_photo(
        FSInputFile(resource.images.get('directions')),
        reply_markup=await kb.directions()
    )
