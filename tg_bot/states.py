from aiogram.fsm.state import StatesGroup, State


class RegisterUser(StatesGroup):
    start_register = State()
    name = State()
    phone = State()
    email = State()
    category = State()
    end_register = State()
    change_date = State()


class MonitoringDate(StatesGroup):
    wait_new_date = State()
    invitation = State()
    end_monitoring = State()


class Edite(StatesGroup):
    is_edite = State()
