import requests

from django.conf import settings

from settings.celery import app
from .models import *
from .serializers import *


@app.task
def registration(public_key: str, subject_name: str) -> None:

    response = requests.post(
        f'{settings.CERTIFICATION_ADDRESS}/api/registration/',
        data={
            'subject_name': subject_name,
            'public_key': public_key,
        })

    response.raise_for_status()

    serializer = CertificateSerializer(data=response.json())
    serializer.is_valid(raise_exception=True)
    serializer.save()

    subject = Subject.objects.get(subject_name=subject_name)
    HistoryRegistration.objects.create(
        subject=subject,
        certificate_serial_number=serializer.validated_data['serial_number']
    )

    #Отправка сертификата субъекту
    return None


@app.task
def cancellation(subject_name: str, code: int) -> None:

    response = requests.post(
        f'{settings.CERTIFICATION_ADDRESS}/api/cancellation',
        data={
            'subject_name':subject_name,
            'code': code
        })

    response.raise_for_status()

    serializer = ResponseCancelledSerializer(data=response.json())
    serializer.is_valid(raise_exception=True)

    serial_number = serializer.validated_data['serial_number']
    code = serializer.validated_data['code']

    certificate = Certificate.objects.get(serial_number=serial_number)
    canc_certificate = As()
    canc_certificate.certificate_serial_number = certificate.serial_number
    canc_certificate.reason_code = str(code)
    canc_certificate.save()

    sas = Sas.objects.all().first()
    sas.certificate.add(canc_certificate)
    sas.save()
    certificate.delete()

    #Отправка информации клиенту об аннулировании
    return None





