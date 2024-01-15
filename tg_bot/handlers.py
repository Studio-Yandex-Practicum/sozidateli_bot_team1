import re

from aiogram import F, Router, types
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

import kb
import text


class RegisterUser(StatesGroup):
    start_register = State()
    name = State()
    phone = State()
    email = State()
    category = State()
    end_register = State()


router = Router()


@router.message(Command('start'))
async def start_handler(msg: Message):
    await msg.answer(text.greet.format(name=msg.from_user.full_name),
                     reply_markup=kb.invitation_to_a_meeting_kb)


@router.callback_query(F.data == 'agree')
async def agree(clbck: types.CallbackQuery, state: FSMContext):
    await clbck.message.answer(text.get_info)
    await clbck.message.answer('Введите ваше имя')
    await state.set_state(RegisterUser.start_register)
    await clbck.message.edit_reply_markup()


@router.message(RegisterUser.start_register, F.text)
async def get_name(msg: Message, state: FSMContext):
    name = msg.text
    if re.match(r'\w', name):
        await state.update_data(name=name)
        await msg.answer('Введите номер телефона в формате +7xxxxxxxxxx')
        await state.set_state(RegisterUser.name)
    else:
        await msg.answer('Имя должно состоять только из букв')


@router.message(RegisterUser.name, F.text)
async def get_phone(msg: Message, state: FSMContext):
    phone = msg.text
    if re.match(r'\+7[0-9]{10}',
                phone):
        await state.update_data(phone=phone)
        await msg.answer('Введите адрес электронной почты')
        await state.set_state(RegisterUser.phone)
    else:
        await msg.answer('Номер телефона указан неверно')


@router.message(RegisterUser.phone, F.text)
async def get_email(msg: Message, state: FSMContext):
    email = msg.text
    if re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b',
                email):
        await state.update_data(email=email)
        await msg.answer('Выберите категорию', reply_markup=kb.categories_kb)
        await state.set_state(RegisterUser.email)
    else:
        await msg.answer('Почта указана неверно')


@router.callback_query(RegisterUser.email, F.data)
async def get_category(clbck: types.CallbackQuery, state: FSMContext):
    await state.update_data(category=clbck.data)
    await state.set_state(RegisterUser.category)
    user_data = await state.get_data()
    await clbck.message.answer(
        f"""Данные указаны верно?
        Имя: {user_data['name']}
        Телефон: {user_data['phone']}
        Почта: {user_data['email']}
        Кому вы хотите помогать: {user_data['category']}""",
        reply_markup=kb.yes_no_kb)
    await clbck.message.edit_reply_markup()


@router.callback_query(RegisterUser.category, F.data == 'confirm_user_data')
async def save_user(clbck: types.CallbackQuery, state: FSMContext):
    await clbck.message.answer(text.save_message)
    await clbck.message.edit_reply_markup()
    await state.set_state(RegisterUser.end_register)


@router.callback_query(F.data == 'error_in_user_data')
async def return_to_correct(clbck: types.CallbackQuery, state: FSMContext):
    await clbck.message.answer('Давайте попробуем еще раз')
    await clbck.message.answer('Введите ваше имя')
    await state.set_state(RegisterUser.start_register)
    await clbck.message.edit_reply_markup()


@router.callback_query(F.data == 'skip')
async def skip(clbck: types.CallbackQuery):
    await clbck.message.answer('Необходимо записаться на собеседование')
