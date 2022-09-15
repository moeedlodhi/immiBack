from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from authentication.models import User
from services.user_service import create_user

User = get_user_model()
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_user_id_from_payload = api_settings.JWT_PAYLOAD_GET_USER_ID_HANDLER


class CustomJSONWebTokenSerializer(serializers.Serializer):
    
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email', '')
        if User.objects.filter(email=email).first():
            message = 'User already exists'
            raise serializers.ValidationError(message)
       
        return super().validate(attrs)
    
    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        try:
            user_to_create = create_user(email, password)
            payload = jwt_payload_handler(user_to_create)

            return {
                'token': jwt_encode_handler(payload),
                'user': user_to_create
            }

        except:
            message = 'User creation failed'
            raise serializers.ValidationError(message)
        