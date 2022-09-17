from authentication.models import User
from rest_framework_jwt.settings import api_settings


jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


def create_user(email, password):
    user = User(
        email=email
    )
    user.set_password(password)
    user.save()
    return user


def verify_token(token):
    try:
        jwt_decode_handler(token)
        return True
    except Exception:
        raise Exception({
            "error": "error decoding token"
        })
