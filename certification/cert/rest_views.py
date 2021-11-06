from datetime import timedelta
from authentication.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


from django.conf import settings
from .serializers import *
from .models import *
from utils import edit_current_time


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

