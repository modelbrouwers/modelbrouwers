from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as _UserAdmin

from .models import User


class UserAdmin(_UserAdmin):
    list_display = (
        'username', 'email',
        'first_name', 'last_name',
        'date_joined', 'is_staff',
        'is_superuser', 'forumuser_id'
    )
    list_editable = ('email', 'forumuser_id')
    ordering = ['-date_joined', 'username']


admin.site.register(User, UserAdmin)
