from rest_framework import serializers

from .models import Certificate


class RequestRegistrationSerializer(serializers.Serializer):
    subject_name = serializers.CharField(max_length=400)
    public_key = serializers.CharField(max_length=600)


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        exclude = ('active', 'info_cancellation')


class RequestCancelledSerializer(serializers.Serializer):
    subject_name = serializers.CharField(max_length=400)
    code = serializers.IntegerField()


class ResponseCancelledSerializer(serializers.Serializer):
    serial_number = serializers.CharField(max_length=400)
    code = serializers.IntegerField()
