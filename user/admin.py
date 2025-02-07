from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import MyUser 

# Не добавляем поля через UserAdmin.fieldsets,
# а сразу регистрируем модель в админке:
admin.site.register(MyUser, UserAdmin) 