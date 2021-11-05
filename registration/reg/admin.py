from django.contrib import admin

from .models import Key, Sas, As, Certificate, Subject, HistoryRegistration, HistoryGetKey

admin.site.register(Key)


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'subject_name', 'start_time', 'end_time')


@admin.register(Sas)
class SasAdmin(admin.ModelAdmin):
    list_display = ('crl_number',)


@admin.register(As)
class AsAdmin(admin.ModelAdmin):
    list_display = ('certificate_serial_number', 'reason_code')


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('subject_name',)


@admin.register(HistoryRegistration)
class HistoryRegistrationAdmin(admin.ModelAdmin):
    list_display = ('subject', 'attempt_time')


@admin.register(HistoryGetKey)
class HistoryGetKey(admin.ModelAdmin):
    list_display = ('subject', 'object', 'attempt_time')
