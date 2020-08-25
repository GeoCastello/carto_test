from requests.models import Request, Response
from rest_framework import status
from rest_framework.utils import json


class ExternalServiceClientMock:
    @staticmethod
    def create_response(status: int, content=None, headers=None):
        if content is None:
            content = {}
        if headers is None:
            headers = {}
        response = Response()
        response.request = Request()
        response.status_code = status
        response.headers.update(headers)
        if isinstance(content, (bytes, bytearray)):
            response._content = content
        else:
            response._content = json.dumps(content).encode('utf-8')
        return response

    @staticmethod
    def create_response_200(content=None, headers=None):
        if content is None:
            content = {}
        if headers is None:
            headers = {}
        return ExternalServiceClientMock.create_response(status.HTTP_200_OK, content, headers)
