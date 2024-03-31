from aiogram.fsm.state import StatesGroup, State


class SignUpStatesGroup(StatesGroup):
    GET_NAME = State()
    GET_PHONE_NUMBER = State()

    SELECT_DIRECTION = State()
    SELECT_DATE = State()
    SELECT_TIME = State()
