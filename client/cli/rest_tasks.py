import requests

from django.conf import settings

from settings.celery import app
from .serializers import *


@app.task
def registration(subject_name: str, secret_key: str, public_key):

    response = requests.post(
        f'{settings.REGISTRATION_ADDRESS}/api/registration/',
        data={
            'subject_name': subject_name,
            'public_key': public_key,
            'secret_key': secret_key
        }
    )

    response.raise_for_status()


@app.task
def get_key(subject_name: str, object_name: str):

    response = requests.get(
        f'{settings.REGISTRATION_ADDRESS}/api/get-key/',
        data={
            'subject_name': subject_name,
            'object_name': object_name,
        }
    )

    response.raise_for_status()

    serializer = ResponseGetKeySerializer(data=response.json())
    serializer.is_valid(raise_exception=True)
    serializer.save()


@app.task
def check_key(serial_number: str):

    response = requests.get(
        f'{settings.REGISTRATION_ADDRESS}/api/check-key/',
        data={
            'serial_number': serial_number
        }
    )

    response.raise_for_status()

    serializer = ResponseGetKeySerializer(data=response.json())
    serializer.is_valid(raise_exception=True)

    status = serializer.validated_data['status']

    if not status:
        certificate = Certificate.objects.get(serial_number=serial_number)
        certificate.delete()



@app.task
def cancellation(subject_name: str, secret_key: str, code: int):

    response = requests.post(
        f'{settings.REGISTRATION_ADDRESS}/api/cancellation/',
        data={
            'subject_name': subject_name,
            'code': code,
            'secret_key': secret_key
        }
    )

    response.raise_for_status()
