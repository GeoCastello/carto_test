import json
import logging
from datetime import datetime

import requests
import urllib3
from django.conf import settings
from requests import Response
from rest_framework import status

from .decorators import add_headers
from .exceptions import BadRequest, ExpectationFailed, ExternalServiceException, ExternalServiceExceptionFactory

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logger = logging.getLogger(__name__)


class ExternalServiceClient:
    MAX_TIMEOUT = 10

    def __init__(self, base_url, auth_token: str = None, auth_basic: str = None, map_exceptions=True, headers=None,
                 exception_factory=None):
        if base_url.endswith('/') is False:
            base_url += '/'
        self.base_url = base_url
        self.auth_token = auth_token
        self.content_type = 'application/json'
        self.auth_basic = auth_basic
        self.map_exceptions = map_exceptions
        self.headers = headers
        if auth_basic is not None:
            self.auth_basic = tuple(self.auth_basic.split(':'))
            if len(self.auth_basic) < 2:
                raise BadRequest(ExternalServiceException.detail_prefix + ': Bad basic auth credential format, must '
                                                                          'be "user:password"')
        self.exception_factory = exception_factory
        if self.exception_factory is None:
            self.exception_factory = ExternalServiceExceptionFactory

    @add_headers
    def get(self, path, params=None, headers=None):
        return self._make_request('get', path, params, headers)

    @add_headers
    def post(self, path, data={}, params=None, headers=None):
        return self._make_request('post', path, params, headers, data)

    @add_headers
    def put(self, path, data={}, params=None, headers=None):
        return self._make_request('put', path, params, headers, data)

    @add_headers
    def patch(self, path, data={}, params=None, headers=None):
        return self._make_request('patch', path, params, headers, data)

    @add_headers
    def delete(self, path, data={}, params=None, headers=None):
        return self._make_request('delete', path, params, headers, data)

    def _make_request(self, method: str, path: str, params=None, headers=None, data=None):
        full_url = self.base_url + path
        time_init = datetime.now()
        try:
            requests_request_args = {
                'params': params,
                'headers': headers,
                'json': data,
                'timeout': self.MAX_TIMEOUT,
                'verify': False,
                'auth': self.auth_basic
            }
            response = requests.request(method, full_url, **requests_request_args)
            time_delta = self._date_diff_in_miliseconds(time_init, datetime.now())
            body = f'\n - Body: {data}' if settings.DEBUG else ''
            log_message = f'{ExternalServiceException.detail_prefix}: "{method.upper()} {full_url} ' \
                          f'- Params: {params} {body} \n\tExecution time {time_delta} ms'
            logger.info(log_message)

        except Exception as e:
            exception_text = ExternalServiceException.detail_prefix + ': ' + str(e)
            logger.error(exception_text)
            if self.map_exceptions:
                raise ExpectationFailed(exception_text)

            response = Response()
            response.status_code = status.HTTP_417_EXPECTATION_FAILED
            response._content = json.dumps({'detail': f'Server unavailable: {self.base_url}'}).encode('utf-8')
            return response

        return self._map_response(response)

    def _date_diff_in_miliseconds(self, dt1, dt2):
        timedelta = dt2 - dt1
        return timedelta.seconds * 1000 + timedelta.microseconds / 1000

    def _map_response(self, response):
        if not str(response.status_code).startswith('2'):
            logger.error(f'External Service Exception: {response.request.method} {response.request.url} - '
                         f'Status:{response.status_code}')
            if self.map_exceptions:
                error_message = f'"{response.request.method} {response.request.url}" - ' \
                                f'Status:{response.status_code} - Body:"{response.text}"'
                exception = self.exception_factory.create_exception(response, error_message)
                raise exception
        return response
