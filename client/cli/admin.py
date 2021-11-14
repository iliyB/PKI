from django.contrib import admin

from .models import Certificate, User


admin.site.register(Certificate)
admin.site.register(User)
