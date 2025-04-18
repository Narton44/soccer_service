from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import CustomUser


class CustomUserAdmin(BaseUserAdmin):
    filter_horizontal = [f for f in BaseUserAdmin.filter_horizontal]
    list_filter = [f for f in BaseUserAdmin.list_filter]

admin.site.register(CustomUser, CustomUserAdmin)