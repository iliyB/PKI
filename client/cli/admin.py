from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import Certificate, Key, File

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
            'date_joined', 'last_login', 'secret_key', 'private_key'
        )}),
    )
    readonly_fields = ('date_joined', 'last_login', 'secret_key')


@admin.register(Key)
class KeyAdmin(admin.ModelAdmin):
    list_display = ('type', 'active')


admin.site.register(Certificate)
admin.site.register(User, CustomUserAdmin)
admin.site.register(File)


