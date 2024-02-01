from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Candidate(models.Model):
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Адрес электронной почты',
        help_text='Электронная почта',
    )
    name = models.CharField(
        max_length=150,
        verbose_name='Имя',
        help_text='Имя',
    )
    telegram_ID = models.CharField(
        primary_key=True,
        max_length=150,
        unique=True,
        blank=True,
        verbose_name='Телеграм_ID',
        help_text='Телеграм_ID',
    )
    phone = models.CharField(
        max_length=12,
        blank=True,
        verbose_name='Номер телефона',
        help_text='Номер телефона',
    )
    category = models.CharField(
        max_length=150,
        verbose_name='Кому помогаем',
        help_text='Кому помогаем',
    )
    confirm_date = models.DateTimeField(
        null=True,
        verbose_name='Дата и время проведения встречи',
        help_text='Дата и время проведения встречи',
    )

    class Meta:
        verbose_name = 'Кандидат'
        verbose_name_plural = 'Кандидаты'

    def __str__(self):
        return self.name
