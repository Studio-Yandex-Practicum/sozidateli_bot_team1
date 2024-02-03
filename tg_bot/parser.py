from datetime import datetime

import requests
from bs4 import BeautifulSoup

from constants import SITE_URL


def parse_meeting_date_time():
    """Получение даты встречи с сайта."""

    response = requests.get(SITE_URL)
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

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        meeting_text = soup.find('meta', {'property': 'og:description'}).get(
            'content')

        date_time_str = (
            meeting_text.split('Открытая встреча состоится')[1].split(
                '. Вам')[0].strip())
        for ru_month, en_month in month_translation.items():
            date_time_str = date_time_str.replace(ru_month, en_month)

        meeting_datetime = datetime.strptime(date_time_str, '%d %B в %H.%M')
        current_datetime = datetime.now()
        meeting_datetime = meeting_datetime.replace(year=current_datetime.year)

        return meeting_datetime

    print(f"Ошибка {response.status_code} при получении страницы.")
    return None


# meeting_datetime = parse_meeting_date_time()

# if meeting_datetime:
#     print(f'Дата и время встречи: {meeting_datetime}')
