# Generated by Django 4.2.9 on 2024-01-20 17:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0005_remove_meeting_candidate'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='meeting',
            options={'ordering': ('-date_meeting',), 'verbose_name': 'Встреча', 'verbose_name_plural': 'Встречи'},
        ),
    ]