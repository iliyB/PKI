import requests
from Crypto.PublicKey import RSA

from django.conf import settings

from settings.celery import app
from cert.models import Key, Certificate
from cert.utils import edit_current_time

from cert.models import InfoCancellation


@app.task
def periodic_cancellation():
    cancl = Certificate.objects.filter(end_time__lt=edit_current_time())

    array = []

    for cert in cancl:
        cert.status = False
        info = InfoCancellation.objects.create(
            revocation_date=edit_current_time(),
            reason_code=6,
            invalidity_date=edit_current_time()
        )
        cert.info_cancellation = info
        cert.save()
        array.append(cert.serial_number)

    response = requests.post(
        f'{settings.REGISTRATION_ADDRESS}/api/periodic-canc/',
        data={
            'array': array
        }
    )

    response.raise_for_status()


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