from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import Certificate


User = get_user_model()

class CustomUserAdmin(UserAdmin):
    list_display = (
        'id', 'username', 'first_name', 'last_name',
        'date_joined', 'is_active')
    search_fields = (
        'username', 'first_name', 'last_name')
    fieldsets = (
        (None, {'fields': (
            'username', 'email', 'password', 'first_name',
            'last_name', 'is_active', 'certificate', 'certificates',
            'date_joined', 'last_login'
        )}),
    )
    readonly_fields = ('date_joined', 'last_login')


admin.site.register(Certificate)
admin.site.register(User, CustomUserAdmin)
