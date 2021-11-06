from rest_framework import serializers

from .models import Subject, Certificate


class RequestRegistrationSerializer(serializers.ModelSerializer):
    public_key = serializers.CharField(max_length=400)

    class Meta:
        model = Subject
        fields = ('__all__')


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


class GetKeySerializer(serializers.ModelSerializer):
    object_name = serializers.CharField(max_length=400)

    class Meta:
         model = Subject
         fields = ('address', 'subject_name', 'object_name')


class CheckKeySerializer(serializers.Serializer):
    serial_number = serializers.CharField(max_length=400)


class RequestCancelledSerializer(serializers.ModelSerializer):
    code = serializers.IntegerField()

    class Meta:
        model = Subject
        fields = ('__all__')


class ResponseCancelledSerializer(serializers.Serializer):
    serial_number = serializers.CharField(max_length=400)
    code = serializers.IntegerField()
