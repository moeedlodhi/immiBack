from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from infrastructure.response import CustomResponse
# Create your views here.


class SubmitQuestionnaire(GenericAPIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        return CustomResponse(status=status.HTTP_201_CREATED, message='OK')
