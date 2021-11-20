from django.contrib import admin

from .models import Certificate, InfoCancellation, Key


admin.site.register(InfoCancellation)


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'subject_name', 'start_time', 'end_time')


@admin.register(Key)
class KeyAdmin(admin.ModelAdmin):
    list_display = ('type', 'active')
