from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from ailock.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'user_type', 'is_staff')
    list_filter = ('user_type', 'is_staff')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('user_type', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'user_type', 'is_staff'),
        }),
    )
    search_fields = ('email',)
    filter_horizontal = ('groups', 'user_permissions')
