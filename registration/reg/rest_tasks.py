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
    



