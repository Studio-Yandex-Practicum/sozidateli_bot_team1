# Generated by Django 4.2.9 on 2024-01-20 16:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_candidate_text_candidate_category_and_more'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='candidate',
            managers=[
            ],
        ),
        migrations.RemoveField(
            model_name='candidate',
            name='date_joined',
        ),
        migrations.RemoveField(
            model_name='candidate',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='candidate',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='candidate',
            name='is_staff',
        ),
        migrations.RemoveField(
            model_name='candidate',
            name='is_superuser',
        ),
        migrations.RemoveField(
            model_name='candidate',
            name='last_login',
        ),
        migrations.RemoveField(
            model_name='candidate',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='candidate',
            name='password',
        ),
        migrations.RemoveField(
            model_name='candidate',
            name='user_permissions',
        ),
    ]