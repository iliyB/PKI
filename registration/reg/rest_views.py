from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .serializers import *
from .models import Subject
from .rest_tasks import *


class RegistrationView(APIView):

    def post(self, request):
        serializer = RequestRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        subject_name = serializer.validated_data['subject_name']

        public_key = serializer.validated_data.pop('public_key')
        subject, created = Subject.objects.update_or_create(**serializer.validated_data)

        if Certificate.objects.filter(subject_name=subject_name).exists():
            HistoryRegistration.objects.create(subject=subject, status=False)
            return Response(status=status.HTTP_400_BAD_REQUEST)

        registration.delay(public_key, subject_name)

        return Response(status=status.HTTP_200_OK)


class GetKeyView(APIView):

    def post(self, request):
        serializer = GetKeySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        object_name = serializer.validated_data['object_name']
        subject_name = serializer.validated_data['subject_name']
        if Certificate.objects.filter(subject_name=object_name).exists():
            object, _ = Subject.objects.get_or_create(subject_name=object_name)
            subject, _ = Subject.objects.get_or_create(subject_name=subject_name)
            HistoryGetKey.objects.create(subject=subject, object=object)
            certificate = Certificate.objects.get(subject_name=object_name)
            return Response(CertificateSerializer(certificate).data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CheckKeyView(APIView):

    def post(self, request):
        serializer = CheckKeySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serial_number = serializer.validated_data['serial_number']
        if Certificate.objects.filter(serial_number=serial_number).exists():
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class CancelledView(APIView):

    def post(self, request):
        serializer = RequestCancelledSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        subject_name = serializer.validated_data['subject_name']
        if Subject.objects.filter(subject_name=subject_name).exists():
            subject = Subject.objects.get(subject_name=subject_name)
            if subject.secret_key != serializer.validated_data['secret_key']:
                return Response(status=status.HTTP_403_FORBIDDEN)
            subject.save()

            cancellation.delay(subject_name, serializer.validated_data['code'])
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)
