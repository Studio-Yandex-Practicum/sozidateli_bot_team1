# Generated by Django 4.2.9 on 2024-01-16 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='telegram_ID',
            field=models.CharField(blank=True, help_text='Телеграм_ID', max_length=150, verbose_name='Телеграм_ID'),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='last name'),
        ),
    ]