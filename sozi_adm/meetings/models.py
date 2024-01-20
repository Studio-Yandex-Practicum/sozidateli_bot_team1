from django.db import models


class Meeting(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name='Название встречи',
        help_text='Название встречи',
    )

    date_created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время создание встречи',
        help_text='Дата и время создания встречи',
    )

    date_meeting = models.DateTimeField(
        blank=True,
        # default='2023-11-16 12:28:27.068357',
        verbose_name='Дата и время проведения встречи',
        help_text='Дата и время проведения встречи',
    )

    date_modified_at = models.DateTimeField(
        auto_now_add=False,
        auto_now=True,
        verbose_name='Изменеие в дате/времени встречи',
        help_text='Изменеие в дате/времени встречи',
        )

    location = models.URLField(
        blank=True,
        max_length=200,
        verbose_name='Ссылка на встречу',
        help_text='Ссылка на встречу',
    )

    class Meta:
        verbose_name = 'Встреча'
        verbose_name_plural = 'Встречи'
        ordering = ('date_meeting', )

    def __str__(self):
        return self.name
