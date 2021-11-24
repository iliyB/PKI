from datetime import timedelta

from Crypto.PublicKey import RSA
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


from django.conf import settings
from .serializers import *
from .models import *
from .utils import edit_current_time, create_signature


class RegistrationView(APIView):

    def post(self, request):
        serializers = RequestRegistrationSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        subject_name = serializers.validated_data['subject_name']
        public_key = serializers.validated_data['public_key']

        certificate = Certificate.objects.create(
            serial_number=User.objects.make_random_password(20),
            id_algorithm_signature='sha',
            publisher_name=settings.CERTIFICATION_NAME,
            start_time=edit_current_time(),
            end_time=edit_current_time() + timedelta(days=90),
            subject_name=subject_name,
            public_key=public_key
        )

        sign = {
            'serial_number': certificate.serial_number,
            'id_algorithm_signature': certificate.id_algorithm_signature,
            'publisher_name': certificate.publisher_name,
            'start_time': certificate.start_time,
            'end_time': certificate.end_time,
            'subject_name': certificate.subject_name,
            'public_key': certificate.public_key,
        }

        key = Key.objects.filter(
            active=True,
            type=Key.KeyType.Cert
        ).first()

        private_key = RSA.import_key(
            open(key.private_key.path).read()
        )

        signature = create_signature(private_key, sign)



        certificate.signature = signature
        certificate.save()

        return Response(CertificateSerializer(certificate).data)


class CancelledView(APIView):

    def post(self, request):
        serializers = RequestCancelledSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        subject_name = serializers.validated_data['subject_name']
        code = serializers.validated_data['code']

        if not Certificate.objects.filter(subject_name=subject_name, active=True).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        certificate = Certificate.objects.get(subject_name=subject_name, active=True)
        info = InfoCancellation.objects.create(
            revocation_date=edit_current_time(),
            reason_code=code,
            invalidity_date=edit_current_time()
        )

        certificate.active=False
        certificate.info_cancellation = info
        certificate.save()

        data = {
            'serial_number': certificate.serial_number,
            'code': code
        }
        return Response(data)


class GetRegistrationKeyView(APIView):

    def post(self, request, *args, **kwargs):
        public_key = request.data.get('key')

        key, created = Key.objects.get_or_create(
            active=True,
            type=Key.KeyType.Reg
        )

        if not created:
            return Response(status=200)

        key.public_key.save(
            f'public_key.pem',
            ContentFile(bytes(public_key, encoding='utf8')),
            save=True
        )

        return Response(status=200)
