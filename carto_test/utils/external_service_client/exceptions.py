from django.conf import settings
from django.http import HttpResponse
from rest_framework import status
from rest_framework.exceptions import APIException


class ExternalServiceException(APIException):
    detail_prefix = 'External Service'

    def __init__(self, message=None, debug=None):
        self.detail = self.detail_prefix + ': ' + self.default_detail
        if debug is None:
            debug = settings.DEBUG
        if message is not None and debug:
            self.detail += ' (' + message + ')'


class BadRequest(ExternalServiceException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Bad Request'


class Forbidden(ExternalServiceException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'Forbidden'


class NotFound(ExternalServiceException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Not Found'


class Conflict(ExternalServiceException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'Conflict with data'


class UnsupportedMediaType(ExternalServiceException):
    status_code = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
    default_detail = 'Unsupported media type'


class ExpectationFailed(ExternalServiceException):
    status_code = status.HTTP_417_EXPECTATION_FAILED
    default_detail = 'Unavailable'


class TooManyRequests(ExternalServiceException):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    default_detail = 'Too many requests'


class UnprocessableEntityException(ExternalServiceException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = 'Unprocessable entity'


class ExternalServiceExceptionFactory:
    @staticmethod
    def create_exception(response: HttpResponse, detail: str):
        code = response.status_code

        if code in [status.HTTP_204_NO_CONTENT, status.HTTP_404_NOT_FOUND]:
            return NotFound(detail)

        elif code == status.HTTP_400_BAD_REQUEST:
            return BadRequest(detail)

        elif code == status.HTTP_403_FORBIDDEN:
            return Forbidden(detail)

        elif code == status.HTTP_415_UNSUPPORTED_MEDIA_TYPE:
            return UnsupportedMediaType(detail)

        elif code == status.HTTP_429_TOO_MANY_REQUESTS:
            return TooManyRequests(detail)

        elif code == status.HTTP_422_UNPROCESSABLE_ENTITY:
            return UnprocessableEntityException(detail)

        else:
            return ExpectationFailed(detail)
