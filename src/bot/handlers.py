from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.fsm.context import FSMContext

from src.bot.states import SignUpStatesGroup
from src.bot import keyboards as kb
from src.bot.utils import load_resources, validate_phone_number
from src.bot.db.crud import SessionCrud, UserCrud, SessionRecordCrud

resource = load_resources()

router = Router()


@router.message(CommandStart())
@router.message(F.text == resource.keyboards.get('cancel'))
async def start(message: Message, state: FSMContext):
    """ обработчик команды start
        запуск бота / приветственное сообщение
    """
    await state.clear()
    await message.answer(resource.texts.get('start'), reply_markup=kb.main_keyboard)


@router.message(F.text == resource.keyboards.get('directions'))
@router.message(Command('directions'))
async def directions(message: Message):
    """
     обработчик команды directions
     выводит список направлений
    """
    await message.answer_photo(
        FSInputFile(resource.images.get('directions')),
        reply_markup=await kb.directions()
    )


async def sign_up_directions(message: Message, state: FSMContext):
    """
    <запись на занятие>
    обработчик для выбора направления
     """
    await state.set_state(SignUpStatesGroup.SELECT_DIRECTION)
    await message.answer('Выберите направление', reply_markup=kb.cancel_keyboard)
    await message.answer_photo(
        FSInputFile(resource.images.get('directions')),
        reply_markup=await kb.directions()
    )


@router.message(F.text == resource.keyboards.get('sign_up'))
async def sign_up(message: Message, state: FSMContext):
    """
    Проверка присутствует ли пользователь в БД
     """
    user = await UserCrud().get_by_telegram_id(message.from_user.id)
    if user:
        await sign_up_directions(message, state)
    else:
        await message.answer('Введите ваше имя')
        await state.set_state(SignUpStatesGroup.GET_NAME)


@router.callback_query(SignUpStatesGroup.SELECT_DIRECTION, F.data.startswith('direction__'))
async def sign_up_select_date(callback: CallbackQuery, state: FSMContext):
    """
    <запись на занятие>
    обработчик для выбора даты
     """
    direction_id = callback.data.split('__')[-1]
    sessions = await SessionCrud().filter_by_direction_id(int(direction_id))

    await callback.message.answer(
        'Выберите дату',
        reply_markup=kb.sig_up_keyboard_builder(sessions, 'date'),
    )
    await state.update_data(direction_id=direction_id)
    await state.set_state(SignUpStatesGroup.SELECT_DATE)
    await callback.answer('select')


@router.callback_query(SignUpStatesGroup.SELECT_DATE, F.data.startswith('date__'))
async def sign_up_select_time(callback: CallbackQuery, state: FSMContext):
    """
    <запись на занятие>
    обработчик для выбора времени
     """
    date = callback.data.split('__')[-1]
    direction_id = (await state.get_data()).get('direction_id')
    sessions = await SessionCrud().filter_by_date_direction(direction_id, date)
    await callback.message.answer(
        'Выберите время',
        reply_markup=kb.sig_up_keyboard_builder(sessions, 'time'),
    )
    await state.update_data(date=date)
    await state.set_state(SignUpStatesGroup.SELECT_TIME)


@router.callback_query(SignUpStatesGroup.SELECT_TIME, F.data.startswith('time__'))
async def sign_up_create_record(callback: CallbackQuery, state: FSMContext):
    """
    <запись на занятие>
    обработчик для сохранения информации о записи в БД
     """
    session_id = callback.data.split('__')[-1]

    user = await UserCrud().get_by_telegram_id(callback.from_user.id)
    session = SessionCrud().get(int(session_id))

    await SessionRecordCrud().create(
        user=user,
        session=session
    )
    await callback.message.answer('Поздравляю! Вы записаны на занятие', reply_markup=kb.main_keyboard)
    await state.clear()


@router.message(SignUpStatesGroup.GET_NAME)
async def user_get_name(message: Message, state: FSMContext):
    """
    <регистрация пользователя>
    обработчик для получения имени пользователя
     """
    await state.update_data(user_name=message.text)
    await state.set_state(SignUpStatesGroup.GET_PHONE_NUMBER)
    await message.answer('Введите номер телефона')


@router.message(SignUpStatesGroup.GET_PHONE_NUMBER)
async def user_get_phone_number(message: Message, state: FSMContext):
    """
    <регистрация пользователя>
    обработчик для получения ноимера телефона и добавления пользователя в БД
     """
    phone_number = validate_phone_number(message.text)
    state_data = await state.get_data()
    if phone_number:
        await UserCrud().create(
            name=state_data.get('user_name'),
            phone_number=phone_number,
            tg_id=message.from_user.id,
        )
        await sign_up_directions(message, state)
    else:
        await message.answer('не верный формат номера!')
