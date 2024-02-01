import datetime as dt
import requests
from aiogram.types import ReplyKeyboardMarkup

from config import config
from constants import STANDART_URL_DJANGO, DOCKER_URL

debug = config.debug
admins = list(map(int, config.admins.split()))


def creare_keyboard(buttons):
    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=True
    )


def get_base_url() -> str:
    if debug:
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
