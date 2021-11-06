from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .serializers import *
from .models import *
from .rest_tasks import *


class RequestRegistrationView(APIView):

    def post(self, request):
        serializer = RequestRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        subject_name = serializer.validated_data['subject_name']

        public_key = serializer.validated_data.pop('public_key')
        subject, created = Subject.objects.create_or_update(**serializer.validated_data)

        if Certificate.objects.filter(subject_name=subject_name).exists():
            HistoryRegistration.objects.create(subject, status=False)
            return Response(status=status.HTTP_400_BAD_REQUEST)

        registration.delay(public_key, subject_name)

        return Response(status=status.HTTP_200_OK)


class GetKeyView(APIView):

    def get(self, request):
        serializer = GetKeySerializer(default=request.data)
        serializer.is_valid(raise_exception=True)
        object_name = serializer.validated_data['object_name']
        subject_name = serializer.validated_data['subject_name']
        if Certificate.objects.filter(subject_name=object_name).exists():
            object, _ = Subject.objects.get_or_create(subject_name=object_name)
            subject, _ = Subject.objects.get_or_create(subject_name=subject_name)
            HistoryGetKey.objects.create(subjec=subject, object=object)
            certificate = Certificate.objects.get(subject_name=object_name)
            return Response(CertificateSerializer(certificate).data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CheckKeyView(APIView):

    def get(self, request):
        serializer = CheckKeySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serial_number = serializer.validated_data['serial_number']
        if Certificate.objects.filter(serial_number=serial_number).exists():
            return Response(data={'status': 'True'}, status=status.HTTP_200_OK)
        else:
            return Response(data={'status': 'False'}, status=status.HTTP_200_OK)


class RequestCancelledView(APIView):

    def post(self, request):
        serializer = RequestCancelledSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        subject_name = serializer.validated_data['subject_name']
        if Subject.objects.filter(subject_name=subject_name).exists():
            subject = Subject.objects.get(subject_name=subject_name)
            if subject.secret_key != serializer.validated_data['secret_key']:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            subject.address = serializer.validated_data['address']
            subject.save()

            #Отправка запроса на аннулированние
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class ResponseCancelledView(APIView):

    def post(self, request):
        serializer = ResponseCancelledSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serial_number = serializer.validated_data['serial_number']
        code = serializer.validated_data['code']

        certificate = Certificate.objects.get(serial_number=serial_number)
        canc_certificate = As()
        canc_certificate.certificate_serial_number = certificate.serial_number
        canc_certificate.reason_code = str(code)
        canc_certificate.save()

        sas = Sas.objects.all().first()
        sas.certificate.add(canc_certificate)
        sas.save()
        certificate.delete()

        return Response(status=status.HTTP_200_OK)