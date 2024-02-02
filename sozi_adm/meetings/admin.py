from django.contrib import admin

from .models import Meeting


@admin.register(Meeting)
class PostAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_meeting', 'location',)
    empty_value_display = '-пусто-'
