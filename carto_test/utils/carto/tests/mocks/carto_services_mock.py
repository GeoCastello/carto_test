import os

from rest_framework.utils import json

from carto_test.utils.external_service_client.mocks.external_service_client_mock import ExternalServiceClientMock


def get_mocked_data(data_type: str = 'stations') -> json:
    current_path = os.path.dirname(__file__)
    if data_type == 'stations':
        with open(f'{current_path}/test_airquality_stations.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    elif data_type == 'measurements':
        with open(f'{current_path}/test_airquality_measurements.json', 'r', encoding='utf-8') as file:
            return json.load(file)


class CartoServicesMock(ExternalServiceClientMock):
    def __init__(self, headers):
        super().__init__(headers)

    @staticmethod
    def create_response_200(content='', service=None):
        if service is None:
            return ExternalServiceClientMock.create_response_200(content=content)
        else:
            content = get_mocked_data(service)

        return ExternalServiceClientMock.create_response_200(content=content)
