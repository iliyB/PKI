from rest_framework import serializers

from .models import Certificate


class RequestRegistrationSerializer(serializers.Serializer):
    subject_name = serializers.CharField(max_length=50)
    secret_key = serializers.CharField(max_length=50)
    public_key = serializers.CharField(max_length=500)


class RequestCancelledSerializer(serializers.Serializer):
    subject_name = serializers.CharField(max_length=50)
    secret_key = serializers.CharField(max_length=50)
    code = serializers.IntegerField()


class RequestGetKeySerializer(serializers.Serializer):
    subject_name = serializers.CharField(max_length=400)
    object_name = serializers.CharField(max_length=400)


class RequestCheckKeySerializer(serializers.Serializer):
    serial_number = serializers.CharField(max_length=400)


class ResponseRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = ('__all__')


class ResponseCancelledSerializer(serializers.Serializer):
    serial_number = serializers.CharField(max_length=400)
    code = serializers.IntegerField()


class ResponseGetKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = ('__all__')


class ResponseCheckKey(serializers.Serializer):
    status = serializers.BooleanField()
