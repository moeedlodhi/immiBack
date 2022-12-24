from calendar import timegm
from datetime import datetime, timedelta
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from authentication.models import User
from services.user_service import create_user, verify_token
from django.db import transaction
from django.contrib.auth import authenticate
from rest_framework_jwt.serializers import VerificationBaseSerializer

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


class JSONRefreshWebTokenSerializer(VerificationBaseSerializer):
    def validate(self, attrs):
        token = attrs['token']
        payload = self._check_payload(token=token)
        user = self._check_user(payload=payload)
        # Get and check 'orig_iat'
        orig_iat = payload.get('orig_iat')
        exp = payload.get('exp')
        now_timestamp = timegm(datetime.utcnow().utctimetuple())
        if exp-now_timestamp < 0:
            raise serializers.ValidationError('Token is expired')
        if exp-now_timestamp < 120 and exp-now_timestamp > 0:
            if orig_iat:

                # Verify expiration
                refresh_limit = api_settings.JWT_REFRESH_EXPIRATION_DELTA

                if isinstance(refresh_limit, timedelta):
                    refresh_limit = (refresh_limit.days * 24 * 3600 +
                                     refresh_limit.seconds)

                expiration_timestamp = orig_iat + int(refresh_limit)
                now_timestamp = timegm(datetime.utcnow().utctimetuple())
                if now_timestamp > expiration_timestamp:
                    msg = ('Refresh has expired.')
                    raise serializers.ValidationError(msg)
            else:
                msg = ('orig_iat field is required.')
                raise serializers.ValidationError(msg)

            new_payload = jwt_payload_handler(user)
            new_payload['orig_iat'] = orig_iat
            return {
                'token': jwt_encode_handler(new_payload),
                'user': user
            }
        else:
            return {
                'token': token,
                'user': user
            }
