from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from authentication.models import User
from services.user_service import create_user, verify_token
from django.db import transaction
from django.contrib.auth import authenticate

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_user_id_from_payload = api_settings.JWT_PAYLOAD_GET_USER_ID_HANDLER


class CustomJSONVerifyTokenSerializer(serializers.Serializer):

    token = serializers.CharField()

    def validate(self, attrs):
        token = attrs.get('token', '')

        try:
            verify_token(token)
        except Exception:
            raise serializers.ValidationError({
                "error": "failed to decode token"
            })

        return token


class CustomJSONWebTokenSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email', '')
        if User.objects.filter(email=email).first():
            message = 'User already exists'
            raise serializers.ValidationError(message)

        return super().validate(attrs)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        payload = jwt_payload_handler(instance)
        token = jwt_encode_handler(payload)
        representation['token'] = token

        return representation

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        with transaction.atomic():
            try:
                user_to_create = create_user(email, password)
                return user_to_create
            except Exception as e:
                message = str(e)
                raise serializers.ValidationError(message)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    @property
    def object(self):
        return self.validated_data

    def validate(self, attrs):

        credentials = {
            "email": attrs.get('email'),
            "password": attrs.get('password')
        }
        user = authenticate(**credentials)
        if user:
            payload = jwt_payload_handler(user)

            return {
                'token': jwt_encode_handler(payload),
                'user': user
            }

        else:
            raise serializers.ValidationError({
                "error": "Incorrect details"
            })
