# flake8: noqa

from aiogram.types import (InlineKeyboardButton,
                           InlineKeyboardMarkup,
                          )

invitation_to_a_meeting = [
    [InlineKeyboardButton(text='Да, я пойду', callback_data='agree'),
    InlineKeyboardButton(text='Я твердо решил стать добровольцем', callback_data='skip')],
]
invitation_to_a_meeting_kb = InlineKeyboardMarkup(inline_keyboard=invitation_to_a_meeting)

categories = [
    [InlineKeyboardButton(text='Детям в больницах', callback_data='Детям в больницах')],
    [InlineKeyboardButton(text='Детям в детских домах', callback_data='Детям в детских домах')],
    [InlineKeyboardButton(text='Семьям с детьми-инвалидами', callback_data='Семьям с детьми-инвалидами')],
    [InlineKeyboardButton(text='Могу автоволонтерить', callback_data='Могу автоволонтерить')],
    [InlineKeyboardButton(text='Еще не решил', callback_data='Еще не решил')],
]
categories_kb = InlineKeyboardMarkup(inline_keyboard=categories)

yes_no = [
    [InlineKeyboardButton(text='Да', callback_data='confirm_user_data')],
    [InlineKeyboardButton(text='Нет', callback_data='error_in_user_data')],
]
yes_no_kb = InlineKeyboardMarkup(inline_keyboard=yes_no)
