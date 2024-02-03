from aiogram.types import KeyboardButton

categories = [
    [KeyboardButton(text='Детям в больницах'),
     KeyboardButton(text='Детям в детских домах')],
    [KeyboardButton(text='Семьям с детьми-инвалидами'),
     KeyboardButton(text='Могу автоволонтерить')],
    [KeyboardButton(text='Еще не решил')],
]

yes_no = [
    [KeyboardButton(text='Да'),
     KeyboardButton(text='Нет')],
    [KeyboardButton(text='Отмена')],
]

invitation_to_a_meeting = [
    [KeyboardButton(text='Записаться на встречу')],
    [KeyboardButton(text='Заполнить анкету, время выберу позже')],
    [KeyboardButton(text='Записаться на собеседование')],
    [KeyboardButton(text='Подробнее о нас')],
]

cancel = [
    [KeyboardButton(text='Отмена')],
]

ok = [
    [KeyboardButton(text='Хорошо')],
]

admin_main = [
    [KeyboardButton(text='(Админ) Список кандидатов')],
    [KeyboardButton(text='(Админ) Изменить дату встречи')],
]

profile_fileds = [
    [KeyboardButton(text='Имя'),
     KeyboardButton(text='Телефон')],
    [KeyboardButton(text='Электронную почту')],
    [KeyboardButton(text='Закончить редактирование')],
]

start = [
    [KeyboardButton(text='/start')],
]
