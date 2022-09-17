from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.status import (
    is_informational, is_success,
    is_redirect, is_client_error, is_server_error
)


class CustomResponse(Response):

    def __init__(self, data: object = None, status: object = None,
                 message: object = None,
                 template_name: object = None, headers: object = None,
                 exception: object = False, content_type: object = None) -> object:

        super(CustomResponse, self).__init__(None, status=status)

        if isinstance(data, Serializer):
            msg = (
                'You passed a Serializer instance as data, but '
                'probably meant to pass serialized `.data` or '
                '`.error`. representation.'
            )
            raise AssertionError(msg)

        status_message = ""
        if is_informational(status):
            status_message = "informational"
        elif is_success(status):
            status_message = "ok"
        elif is_redirect(status):
            status_message = "redirect"
        elif is_client_error(status):
            status_message = "client_error"
        elif is_server_error(status):
            status_message = "server_error"

        self.data = {
            'data': data,
            'status_message': status_message,
            'message': message
        }
        self.template_name = template_name
        self.exception = exception
        self.content_type = content_type

        if headers:
            for name, value in headers.items():
                self[name] = value
