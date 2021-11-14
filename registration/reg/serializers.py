from rest_framework import serializers

from .models import Subject, Certificate


class RequestRegistrationSerializer(serializers.ModelSerializer):
    public_key = serializers.CharField(max_length=400)

    class Meta:
        model = Subject
        exclude = ('address',)


# class SendRegistrationSerializer(serializers.ModelSerializer):
#     public_key = serializers.CharField(max_length=400)
#
#     class Meta:
#         model = Subject
#         fields = ('subject_name', 'public_key')


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = ('__all__')


class GetKeySerializer(serializers.Serializer):
    subject_name = serializers.CharField(max_length=400)
    object_name = serializers.CharField(max_length=400)


class CheckKeySerializer(serializers.Serializer):
    serial_number = serializers.CharField(max_length=400)


class RequestCancelledSerializer(serializers.ModelSerializer):
    code = serializers.IntegerField()

    class Meta:
        model = Subject
        exclude = ('address',)


class ResponseCancelledSerializer(serializers.Serializer):
    serial_number = serializers.CharField(max_length=400)
    code = serializers.IntegerField()

