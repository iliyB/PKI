from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .serializers import *
from .models import Certificate


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
        user = User.objects.get(username=certificate.subject_name)
        user.certificate = certificate
        user.save()

        return Response(status=status.HTTP_200_OK)
