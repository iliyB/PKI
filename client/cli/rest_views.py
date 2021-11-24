from Crypto.PublicKey import RSA
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .serializers import *
from .models import Certificate, Key
from .utils import check_signature


class CancelledView(APIView):

    def post(self, request, *args, **kwargs):
        serializers = ResponseCancelledSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        
        serial_number = serializers.validated_data['serial_number']
        
        certificate = Certificate.objects.get(serial_number=serial_number)
        certificate.delete()

        return Response(status=status.HTTP_200_OK)


class RegistrationView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = ResponseRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        signature = serializer.validated_data['signature']
        # signature = bytes(signature, encoding='utf8')

        key = Key.objects.filter(
            active=True,
            type=Key.KeyType.Cert
        ).first()

        public_key = RSA.import_key(
            open(key.public_key.path).read()
        )

        sign = {
            'serial_number': serializer.validated_data['serial_number'],
            'id_algorithm_signature': serializer.validated_data['id_algorithm_signature'],
            'publisher_name': serializer.validated_data['publisher_name'],
            'start_time': serializer.validated_data['start_time'],
            'end_time': serializer.validated_data['end_time'],
            'subject_name': serializer.validated_data['subject_name'],
            'public_key': serializer.validated_data['public_key'],
        }

        if not not check_signature(public_key, sign, signature):
            return Response(status=400)

        certificate = serializer.save()
        user = get_user_model().objects.get(username=certificate.subject_name)
        user.certificate = certificate
        user.save()

        return Response(status=status.HTTP_200_OK)


class GetCertificationKeyView(APIView):

    def post(self, request, *args, **kwargs):
        public_key = request.data.get('key')

        key, created = Key.objects.get_or_create(
            active=True,
            type=Key.KeyType.Cert
        )

        if not created:
            return Response(status=200)

        key.public_key.save(
            f'public_key.pem',
            ContentFile(bytes(public_key, encoding='utf8')),
            save=True
        )

        return Response(status=200)
