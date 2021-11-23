import requests
from Crypto.PublicKey import RSA

from django.conf import settings

from settings.celery import app

from cert.models import Key


@app.task
def send_key_cli():

    key = Key.objects.filter(
        active=True,
        type=Key.KeyType.Cert
    ).first()


    public_key = RSA.import_key(
        open(key.public_key.path).read()
    )

    public_key = public_key.export_key('PEM').decode()

    response = requests.post(
        f'{settings.CLIENT_ADDRESS}/api/cert-key/',
        data={
            'key': public_key
        }
    )

    response.raise_for_status()


@app.task
def send_key_reg():

    key = Key.objects.filter(
        active=True,
        type=Key.KeyType.Cert
    ).first()


    public_key = RSA.import_key(
        open(key.public_key.path).read()
    )

    public_key = public_key.export_key('PEM').decode()

    response = requests.post(
        f'{settings.REGISTRATION_ADDRESS}/api/cert-key/',
        data={
            'key': public_key
        }
    )

    response.raise_for_status()