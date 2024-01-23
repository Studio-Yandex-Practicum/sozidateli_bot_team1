import datetime as dt
import re
import requests

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

import keyboards
from states import RegisterUser
import constants
from utils import creare_keyboard


router = Router()


@router.message(Command('start'))
async def start_handler(msg: Message, state: FSMContext):
    
    date_of_meeting = requests.get('http://admin:8000/api/meeting/')
    date_of_meeting = dt.datetime.strptime(
        date_of_meeting.json()[0].get('date_meeting'), "%Y-%m-%dT%H:%M:%SZ"
    )
    
    await state.update_data(date_meeting=date_of_meeting)
    await msg.answer(
        constants.GREET.format(name=msg.from_user.full_name,
                               date=date_of_meeting,
                               time=date_of_meeting),
        reply_markup=creare_keyboard(keyboards.invitation_to_a_meeting))


@router.message(F.text == 'Записаться на встречу')
async def agree(msg: Message, state: FSMContext):
    await msg.answer(constants.GET_INFO)
    await msg.answer(constants.GET_NAME,
                     reply_markup=creare_keyboard(keyboards.cancel))
    await state.set_state(RegisterUser.start_register)


@router.message(RegisterUser.start_register, F.text != 'Отмена')
async def get_name(msg: Message, state: FSMContext):
    name = msg.text
    if re.match(r'\w', name):
        await state.update_data(user_id=msg.chat.id)
        await state.update_data(name=name)
        await msg.answer(constants.GET_PHONE,
                         reply_markup=creare_keyboard(keyboards.cancel))
        await state.set_state(RegisterUser.name)
    else:
        await msg.answer(constants.ERROR_IN_NAME)


@router.message(RegisterUser.name, F.text != 'Отмена')
async def get_phone(msg: Message, state: FSMContext):
    phone = msg.text
    if re.match(r'\+7[0-9]{10}',
                phone):
        await state.update_data(phone=phone)
        await msg.answer(constants.GET_EMAIL,
                         reply_markup=creare_keyboard(keyboards.cancel))
        await state.set_state(RegisterUser.phone)
    else:
        await msg.answer(constants.ERROR_IN_PHONE)


@router.message(RegisterUser.phone, F.text != 'Отмена')
async def get_email(msg: Message, state: FSMContext):
    email = msg.text
    if re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b',
                email):
        await state.update_data(email=email)
        await msg.answer(constants.CHOOSE_CATEGORY,
                         reply_markup=creare_keyboard(keyboards.categories))
        await state.set_state(RegisterUser.email)
    else:
        await msg.answer(constants.ERROR_IN_EMAIL)


@router.message(RegisterUser.email, F.text != 'Отмена')
async def get_category(msg: Message, state: FSMContext):
    await state.update_data(category=msg.text,
                            telegram_ID=msg.from_user.id)
    await state.set_state(RegisterUser.category)
    user_data = await state.get_data()
    await msg.answer(
        constants.CHECK_DATA.format(
            name=user_data['name'],
            phone=user_data['phone'],
            email=user_data['email'],
            category=user_data['category']),
        reply_markup=creare_keyboard(keyboards.yes_no))


@router.message(RegisterUser.category, F.text == 'Да')
async def save_user(msg: Message, state: FSMContext):
    user_data = await state.get_data()
    requests.post(
        f'http://admin:8000/api/candidate/{user_data["telegram_ID"]}/',
        user_data
        )
    await msg.answer(constants.SAVE_MESSAGE)
    await state.set_state(RegisterUser.end_register)


@router.message(F.text == 'Нет')
async def return_to_correct(msg: Message, state: FSMContext):
    await msg.answer(constants.ONE_MORE_TIME)
    await msg.answer(constants.GET_NAME)
    await state.set_state(RegisterUser.start_register)


@router.message(F.text == 'Записаться на собеседование')
async def skip(msg: Message):
    await msg.answer(constants.INVITATION_TO_INTERVIEW)


@router.message(F.text == 'Подробнее о нас')
async def about_us(msg: Message):
    await msg.answer(constants.ABOUT_US)


@router.message(F.text == 'Отмена')
async def menu(msg: Message, state: FSMContext):
    await state.set_data({})
    await state.clear()
    await msg.answer(constants.CANCEL_REGISTRATION)
    await msg.answer(
        constants.MENU,
        reply_markup=creare_keyboard(keyboards.invitation_to_a_meeting))
