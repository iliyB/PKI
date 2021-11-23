from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .serializers import *
from .models import Certificate, Key


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
