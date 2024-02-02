import asyncio
import re

import requests
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from requests.exceptions import ConnectionError

import constants
import keyboards
from tg_bot.parser import parse_meeting_date_time
from tg_bot.states import Edite, MonitoringDate, RegisterUser
from tg_bot.utils import (create_keyboard, get_base_url, get_date_of_meeting,
                          is_admin, set_date_of_meeting)

router = Router()


@router.message(Command('start'))
async def start_handler(msg: Message, state: FSMContext):
    """Начало диалога."""
    try:
        date_of_meeting, address = get_date_of_meeting(location=True)
    except ConnectionError:
        await msg.answer(
            constants.CONNECTION_ERROR,
            reply_markup=create_keyboard(keyboards.start)
        )
    if date_of_meeting:
        filler = constants.ADD_DATE_TO_GREET.format(
            date=date_of_meeting.strftime('%d.%m'),
            time=date_of_meeting.strftime('%H:%M'),
            address=address)
        await state.update_data(confirm_date=date_of_meeting)

    else:
        filler = constants.ADD_WITHOUT_DATE

    keyboard = keyboards.admin_main if is_admin(msg.from_user.id) else []
    keyboard.extend(keyboards.invitation_to_a_meeting)
    await msg.answer(
        constants.GREET.format(
            name=msg.from_user.full_name,
            filler=filler
        ),
        reply_markup=create_keyboard(keyboard)
    )


@router.message(F.text == '(Админ) Список кандидатов')
async def admin_user_list(msg: Message, state: FSMContext):
    """Получение списка канидатов. (только для ТГ-администратора.)"""
    if not is_admin(msg.from_user.id):
        await msg.answer(constants.ERROR_NO_PERMISSION)
    base_url = get_base_url()
    response = requests.get(f'{base_url}:8000/api/candidate/').json()
    reply = 'Кандидаты на ближайшую встречу:\n'
    for i, candidate in enumerate(response):
        reply += f'{i+1}. ' + candidate.get('name') + '\n'
    await msg.answer(reply)
    await state.set_state(RegisterUser.start_register)


@router.message(F.text == '(Админ) Изменить дату встречи')
async def admin_change_meeting(msg: Message, state: FSMContext):
    """Изменение даты встречи. (только для ТГ-администратора.)"""

    if not is_admin(msg.from_user.id):
        await msg.answer(constants.ERROR_NO_PERMISSION)

    try:
        old_date = get_date_of_meeting()
    except ConnectionError:
        await msg.answer(
            constants.CONNECTION_ERROR,
            reply_markup=create_keyboard(keyboards.start)
        )
    await msg.answer(f'Текущая встреча запланирована на {old_date}.')

    text = parse_meeting_date_time()
    await msg.answer(f'Для справки:\nНа сайте указана: {text}.')

    keyboard = keyboards.ok
    keyboard.extend(keyboards.cancel)
    await msg.answer(
        'Введите новую дату встречи:',
        reply_markup=create_keyboard(keyboard)
    )
    await state.set_state(RegisterUser.change_date)


@router.message(RegisterUser.change_date, F.text != 'Отмена')
async def admin_set_date(msg: Message, state: FSMContext):
    if not is_admin(msg.from_user.id):
        await msg.answer(constants.ERROR_NO_PERMISSION)

    new_date = msg.text
    if not re.match(r'(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})',
                    new_date):
        await msg.answer(constants.ERROR_IN_DATE)

    response = set_date_of_meeting(msg.text)
    if response.status_code == 200:
        await msg.answer(f'Дата сохранена. {response.text}')

        keyboard = keyboards.admin_main if is_admin(msg.from_user.id) else []
        keyboard.extend(keyboards.invitation_to_a_meeting)

        await state.set_state(
            RegisterUser.start_register,
            reply_markup=create_keyboard(keyboard)
        )
    else:
        await msg.answer(f'Ошибка. {response.text}')


@router.message(F.text == 'Заполнить анкету, время выберу позже')
@router.message(F.text == 'Записаться на встречу')
async def agree(msg: Message, state: FSMContext):
    if msg.text == 'Заполнить анкету, время выберу позже':
        await state.update_data(confirm_date=None)
    await msg.answer(constants.GET_INFO)
    await msg.answer(constants.GET_NAME,
                     reply_markup=create_keyboard(keyboards.cancel))
    await state.set_state(RegisterUser.start_register)


@router.message(RegisterUser.start_register, F.text != 'Отмена')
async def get_name(msg: Message, state: FSMContext):
    name = msg.text
    user_data = await state.get_data()
    if re.match(r'\w', name):
        await state.update_data(user_id=msg.chat.id)
        await state.update_data(name=name)
        if user_data.get('is_edite'):
            await state.set_state(Edite.is_edite)
            await msg.answer(
                constants.CHOOSE_EDITE_FIELD,
                reply_markup=create_keyboard(keyboards.profile_fileds)
            )
        else:
            await msg.answer(constants.GET_PHONE,
                             reply_markup=create_keyboard(keyboards.cancel))
            await state.set_state(RegisterUser.name)
    else:
        await msg.answer(constants.ERROR_IN_NAME)


@router.message(RegisterUser.name, F.text != 'Отмена')
async def get_phone(msg: Message, state: FSMContext):
    phone = msg.text
    user_data = await state.get_data()
    if re.match(r'\+7[0-9]{10}$',
                phone):
        await state.update_data(phone=phone)
        if user_data.get('is_edite'):
            await state.set_state(Edite.is_edite)
            await msg.answer(
                constants.CHOOSE_EDITE_FIELD,
                reply_markup=create_keyboard(keyboards.profile_fileds)
            )
        else:
            await msg.answer(
                constants.GET_EMAIL,
                reply_markup=create_keyboard(keyboards.cancel)
            )
            await state.set_state(RegisterUser.phone)
    else:
        await msg.answer(constants.ERROR_IN_PHONE)


@router.message(RegisterUser.phone, F.text != 'Отмена')
async def get_email(msg: Message, state: FSMContext):
    email = msg.text
    user_data = await state.get_data()
    if re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b',
                email):
        await state.update_data(email=email)
        if user_data.get('is_edite'):
            await state.set_state(Edite.is_edite)
            await msg.answer(
                constants.CHOOSE_EDITE_FIELD,
                reply_markup=create_keyboard(keyboards.profile_fileds)
            )
        else:
            await msg.answer(
                constants.CHOOSE_CATEGORY,
                reply_markup=create_keyboard(keyboards.categories)
            )
            await state.set_state(RegisterUser.email)
    else:
        await msg.answer(constants.ERROR_IN_EMAIL)


@router.message(F.text == 'Закончить редактирование')
@router.message(RegisterUser.email, F.text != 'Отмена')
async def get_category(msg: Message, state: FSMContext):
    if msg.text != 'Закончить редактирование':
        await state.update_data(category=msg.text,
                                telegram_ID=msg.from_user.id)
    await state.set_state(RegisterUser.category)
    user_data = await state.get_data()
    if not user_data.get('confirm_date'):
        await msg.answer(
            constants.CHECK_DATA.format(
                name=user_data['name'],
                phone=user_data['phone'],
                email=user_data['email'],
                category=user_data['category']),
            reply_markup=create_keyboard(keyboards.yes_no))
    else:
        await msg.answer(
            constants.CHECK_DATA.format(
                confirm_date=user_data['confirm_date'],
                name=user_data['name'],
                phone=user_data['phone'],
                email=user_data['email'],
                category=user_data['category']),
            reply_markup=create_keyboard(keyboards.yes_no))


@router.message(RegisterUser.category, F.text == 'Да')
async def save_user(msg: Message, state: FSMContext):
    user_data = await state.get_data()
    base_url = get_base_url()
    try:
        register = requests.post(
            f'{base_url}:8000/api/candidate/',
            user_data
        )
    except ConnectionError:
        await msg.answer(
            constants.CONNECTION_ERROR,
            reply_markup=create_keyboard(keyboards.start)
        )

    if not user_data.get('confirm_date'):
        await state.set_state(MonitoringDate.wait_new_date)
        try:
            old_date = get_date_of_meeting()
        except ConnectionError:
            await msg.answer(
                constants.CONNECTION_ERROR,
                reply_markup=create_keyboard(keyboards.start)
            )
        await state.update_data(confirm_date=old_date)
        await msg.answer(
            constants.SAVE_WITHOUT_DATE,
            reply_markup=create_keyboard(keyboards.ok)
        )
    else:
        if register.status_code == 201:
            await msg.answer(constants.SAVE_MESSAGE)
            await state.set_state(RegisterUser.end_register)
        else:
            errors = constants.ERROR
            for key in register.json():
                errors = errors + register.json()[key][0] + '\n'
            await msg.answer(errors)


@router.message(MonitoringDate.wait_new_date, F.text == 'Хорошо')
async def wait_new_date(msg: Message, state: FSMContext):
    print('BEGIN MONITORING')
    try:
        date_in_db = get_date_of_meeting()
    except ConnectionError:
        await msg.answer(
            constants.CONNECTION_ERROR,
            reply_markup=create_keyboard(keyboards.start)
        )
    user_data = await state.get_data()
    while user_data['confirm_date'] == date_in_db:
        print('ничего нового')
        # now = dt.datetime.now()
        # tomorrow = now + dt.timedelta(days=1)
        # tomorrow_morning = dt.datetime(
        # tomorrow.year,
        # tomorrow.month,
        # tomorrow.day,
        # 10, 00)
        # sleep_time = tomorrow_morning - now
        # await asyncio.sleep(tomorrow_morning)
        await asyncio.sleep(10)
        try:
            date_in_db = get_date_of_meeting()
        except ConnectionError:
            await msg.answer(
                constants.CONNECTION_ERROR,
                reply_markup=create_keyboard(keyboards.start)
            )
    print('дата изменилась')
    await msg.answer(constants.NEW_DATE.format(
        date=date_in_db.strftime('%d.%m'),
        time=date_in_db.strftime('%H:%M')),
        reply_markup=create_keyboard(keyboards.yes_no)
    )
    await state.set_state(MonitoringDate.invitation)
    await state.update_data(confirm_date=date_in_db)


@router.message(MonitoringDate.invitation, F.text == 'Да')
async def upgrade_candidate_confirm_date(msg: Message, state: FSMContext):
    base_url = get_base_url()
    user_data = await state.get_data()
    try:
        update = requests.patch(
            f'{base_url}:8000/api/candidate/{user_data.get("telegram_ID")}/',
            {"confirm_date": user_data['confirm_date']}
        )
    except ConnectionError:
        await msg.answer(
            constants.CONNECTION_ERROR,
            reply_markup=create_keyboard(keyboards.start)
        )
    if update.status_code == 200:
        await msg.answer('Мы вас записали')
        await state.set_state(MonitoringDate.end_monitoring)

    else:
        errors = constants.ERROR
        for key in update.json():
            errors = errors + update.json()[key][0] + '\n'
        await msg.answer(errors)


@router.message(MonitoringDate.invitation, F.text == 'Нет')
async def cancel_new_date(msg: Message, state: FSMContext):
    await msg.answer(constants.WHAIT_NEW_DATE,
                     reply_markup=create_keyboard(keyboards.ok))
    await state.set_state(MonitoringDate.wait_new_date)


@router.message(F.text == 'Нет')
async def return_to_correct(msg: Message, state: FSMContext):
    await msg.answer(constants.CHOOSE_EDITE_FIELD,
                     reply_markup=create_keyboard(keyboards.profile_fileds))
    await state.set_state(Edite.is_edite)


@router.message(Edite.is_edite, F.text)
async def recall_wrong_field(msg: Message, state: FSMContext):
    await state.update_data(is_edite=True)
    if msg.text == 'Имя':
        await msg.answer(constants.GET_NAME,
                         reply_markup=create_keyboard(keyboards.cancel))
        await state.set_state(RegisterUser.start_register)

    if msg.text == 'Телефон':
        await msg.answer(constants.GET_PHONE,
                         reply_markup=create_keyboard(keyboards.cancel))
        await state.set_state(RegisterUser.name)

    if msg.text == 'Электронную почту':
        await msg.answer(constants.GET_EMAIL,
                         reply_markup=create_keyboard(keyboards.cancel))
        await state.set_state(RegisterUser.phone)

    if msg.text == 'Категорию':
        await msg.answer(constants.CHOOSE_CATEGORY,
                         reply_markup=create_keyboard(keyboards.categories))
        await state.set_state(RegisterUser.email)


@router.message(F.text == 'Записаться на собеседование')
async def skip(msg: Message):
    await msg.answer(
        constants.INVITATION_TO_INTERVIEW,
        reply_markup=create_keyboard(keyboards.invitation_to_a_meeting)
    )


@router.message(F.text == 'Подробнее о нас')
async def about_us(msg: Message):
    await msg.answer(
        constants.ABOUT_US,
        reply_markup=create_keyboard(keyboards.invitation_to_a_meeting)
    )


@router.message(F.text == 'Отмена')
async def menu(msg: Message, state: FSMContext):
    await state.set_data({})
    await state.clear()
    await msg.answer(constants.CANCEL_REGISTRATION)
    keyboard = keyboards.admin_main if is_admin(msg.from_user.id) else []
    keyboard.extend(keyboards.invitation_to_a_meeting)
    await msg.answer(
        constants.MENU,
        reply_markup=create_keyboard(keyboard))
