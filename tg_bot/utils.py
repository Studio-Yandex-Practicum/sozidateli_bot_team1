from aiogram.types import ReplyKeyboardMarkup

from constants import STANDART_URL_DJANGO, DOCKER_URL
from django.conf import settings

settings.configure()


def creare_keyboard(buttons):
    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=True
    )


def get_base_url():
    if not settings.DEBUG:
        return STANDART_URL_DJANGO
    return DOCKER_URL
