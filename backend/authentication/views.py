# Create your views here.
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from authentication.serializers import CustomJSONWebTokenSerializer
from authentication.models import User
from infrastructure.auth import JWTAuthentication
from infrastructure.response import CustomResponse


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


class verifyToken(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    queryset = User.objects.all()

    def get(self, request):
        return CustomResponse(status=status.HTTP_200_OK, message='OK')
