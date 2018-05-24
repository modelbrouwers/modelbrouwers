from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as _UserAdmin

from .forms import AdminUserCreationForm
from .models import DataDownloadRequest, User


@admin.register(User)
class UserAdmin(_UserAdmin):
    list_display = (
        'username', 'email',
        'first_name', 'last_name',
        'date_joined', 'is_staff',
        'is_superuser', 'forumuser_id'
    )
    list_editable = ('email', 'forumuser_id')
    ordering = ['-date_joined', 'username']
    add_form = AdminUserCreationForm
    change_form_template = 'loginas/change_form.html'


@admin.register(DataDownloadRequest)
class DataDownloadRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'created', 'finished')
    list_filter = ('created', 'finished')
    list_select_related = ('user',)
    date_hierarchy = 'created'
    search_fields = ('user__id', 'user__username', 'user__email')
    readonly_fields = ('zip_file',)
    raw_id_fields = ('user',)
