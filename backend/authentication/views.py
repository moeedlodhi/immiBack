# Create your views here.
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from authentication.serializers import CustomJSONWebTokenSerializer
from infrastructure.response import CustomResponse


class AuthJsonWebTokeView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CustomJSONWebTokenSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = CustomJSONWebTokenSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return CustomResponse(status=status.HTTP_400_BAD_REQUEST, message=str(serializer.errors))
        return CustomResponse(status=status.HTTP_200_OK, message='OK')
