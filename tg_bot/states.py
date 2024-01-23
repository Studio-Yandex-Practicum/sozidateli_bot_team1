from aiogram.fsm.state import StatesGroup, State


class RegisterUser(StatesGroup):
    start_register = State()
    name = State()
    phone = State()
    email = State()
    category = State()
    end_register = State()
