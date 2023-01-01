# Create your views here.
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from infrastructure.response import CustomResponse
from authentication.serializers import CustomJSONWebTokenSerializer
from authentication.serializers import LoginSerializer
from authentication.serializers import JSONRefreshWebTokenSerializer
from infrastructure.auth import JWTAuthentication


class AuthJsonWebTokeView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CustomJSONWebTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = CustomJSONWebTokenSerializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
            else:
                return CustomResponse(status=status.HTTP_400_BAD_REQUEST, message=str(serializer.errors))
            return CustomResponse(status=status.HTTP_201_CREATED, message='OK', data=serializer.data)
        except Exception as e:
            return CustomResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e))


class verifyToken(GenericAPIView):
    permission_classes = (AllowAny,)
    authentication_classes = (JWTAuthentication,)
    serializer_class = JSONRefreshWebTokenSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return CustomResponse(status=status.HTTP_200_OK, message='OK', data=serializer.data)
        else:
            return CustomResponse(status=status.HTTP_400_BAD_REQUEST, message=str(serializer.errors))


class loginuser(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        try:
            if serializer.is_valid():
                user = serializer.object.get('user')
                token = serializer.object.get('token')
                data = {
                    "user": user.email,
                    "token": token
                }
                return CustomResponse(status=status.HTTP_200_OK, message='OK', data=data)
            else:
                return CustomResponse(status=status.HTTP_400_BAD_REQUEST, message=str(serializer.errors))
        except Exception as e:
            return CustomResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e))
