from django.db import models
from django.contrib.auth.models import AbstractUser


class Candidate(AbstractUser):
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Адрес электронной почты',
        help_text='Электронная почта',
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Юзернейм',
        help_text='Уникальный юзернейм',
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
        help_text='Имя',
    )
    telegram_ID = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Телеграм_ID',
        help_text='Телеграм_ID',
    )
    password = models.CharField(
        max_length=150,
        verbose_name='Пароль',
        help_text='Пароль',
    )
    phone = models.CharField(
        max_length=12,
        blank=True,
        verbose_name='Номер телефона',
        help_text='Номер телефона',
    )

    text = models.BooleanField(
        verbose_name='Хотите познакомиться с нами на открытой встрече?',
        help_text='Хотите познакомиться с нами на открытой встрече?',
        default=True,
    )

    class Meta:
        verbose_name = 'Кандидат'
        verbose_name_plural = 'Кандидаты'

    def __str__(self):
        return self.username

