from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'password', 'icon', 'tag_user_icon')}),
        ('Personal Information', {'fields': ('email',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    readonly_fields = ('tag_user_icon',)
