from aiogram.types import ReplyKeyboardMarkup


def creare_keyboard(buttons):
    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=True
    )
