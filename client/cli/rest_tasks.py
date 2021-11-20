import requests

from django.contrib.auth import get_user_model
from django.conf import settings

from settings.celery import app
from .serializers import *


@app.task
def registration(subject_name: str, secret_key: str, public_key):

    data = {
        'subject_name': subject_name,
        'public_key': public_key,
        'secret_key': secret_key
    }

    response = requests.post(
        f'{settings.REGISTRATION_ADDRESS}/api/registration/',
        data=RequestRegistrationSerializer(data).data
    )

    response.raise_for_status()


@app.task
def get_key(subject_name: str, object_name: str):

    if Certificate.objects.filter(subject_name=object_name).exists():
        instance = Certificate.objects.get(subject_name=object_name)
    else:
        data = {
            'subject_name': subject_name,
            'object_name': object_name,
        }


        response = requests.post(
            '{}/api/get-key/'.format(settings.REGISTRATION_ADDRESS),
            data = RequestGetKeySerializer(data).data
        )

        response.raise_for_status()

        serializer = ResponseGetKeySerializer(data=response.json())
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

    user = get_user_model().objects.get(username=subject_name)
    user.certificates.add(instance)
    user.save()



@app.task
def check_key(serial_number: str):

    data = {
        'serial_number': serial_number
    }

    response = requests.post(
        f'{settings.REGISTRATION_ADDRESS}/api/check-key/',
        data = RequestCheckKeySerializer(data).data
    )

    response.raise_for_status()

    if not response.ok:
        certificate = Certificate.objects.filter(serial_number=serial_number)
        certificate.delete()



@app.task
def cancellation(subject_name: str, secret_key: str, code: int):

    data = {
        'subject_name': subject_name,
        'code': code,
        'secret_key': secret_key
    }

    response = requests.post(
        f'{settings.REGISTRATION_ADDRESS}/api/cancellation/',
        data = RequestCancelledSerializer(data).data
    )

    response.raise_for_status()
