import datetime as dt

import requests
from aiogram.types import ReplyKeyboardMarkup

from config import config
from constants import DOCKER_URL, STANDART_URL_DJANGO

local = config.local
admins = list(map(int, config.admins.split()))


def creare_keyboard(buttons):
    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=True
    )


def get_base_url() -> str:
    if local:
        return STANDART_URL_DJANGO
    return DOCKER_URL


def get_date_of_meeting(location=False):
    base_url = get_base_url()
    response = requests.get(f'{base_url}:8000/api/meeting/').json()[0]
    if response.get('date_meeting'):
        if location:
            return dt.datetime.strptime(
                response.get('date_meeting'), "%Y-%m-%dT%H:%M:%SZ"
            ), response.get('location')
        return dt.datetime.strptime(
            response.get('date_meeting'), "%Y-%m-%dT%H:%M:%SZ"
        )
    return None, None


def set_date_of_meeting(data) -> requests.Response:
    """Обновление даты актуальной встречи."""

    base_url = get_base_url()
    response = requests.patch(
        url=f'{base_url}:8000/api/meeting/',
        data={
            'date_meeting': data
        }
    )
    return response


def is_admin(user_id) -> bool:
    """Проверяем права админа по Telegram-ID."""

    return user_id in admins


def parse_pinned_message(pinned_message):
    month_translation = {
        'января': 'January',
        'февраля': 'February',
        'марта': 'March',
        'апреля': 'April',
        'мая': 'May',
        'июня': 'June',
        'июля': 'July',
        'августа': 'August',
        'сентября': 'September',
        'октября': 'October',
        'ноября': 'November',
        'декабря': 'December'
    }

    pinned_text = pinned_message.text

    date_time_str = (
        pinned_text.split(
            ' - ОТКРЫТАЯ ВСТРЕЧА')[0].strip())
    for ru_month, en_month in month_translation.items():
        date_time_str = date_time_str.replace(ru_month, en_month)

    pinned_datetime = dt.datetime.strptime(date_time_str, '%d %B %H.%M')
    current_datetime = dt.datetime.now()
    pinned_datetime = pinned_datetime.replace(year=current_datetime.year)
    return pinned_datetime
