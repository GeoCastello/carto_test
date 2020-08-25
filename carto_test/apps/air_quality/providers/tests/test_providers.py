from unittest.mock import patch

import requests
from django.test import TestCase

from carto_test.apps.air_quality.models import MeasurementsStatistics
from carto_test.apps.air_quality.providers.statistics_provider import StatisticsProvider
from carto_test.utils.carto.tests.mocks.carto_services_mock import get_mocked_data
from carto_test.utils.external_service_client.mocks.external_service_client_mock import ExternalServiceClientMock


class TestStatisticsProvider(TestCase):

    def setUp(self):
        self.statistics_request = {
            'start_time': '2016-10-05T11:00:00Z',
            'end_time': '2016-11-11T17:47:17Z',
            'variable': 'co',
            'statistical_measurement': 'AVG'
        }
        self.provider = StatisticsProvider(self.statistics_request)

    def test_constructor(self):
        self.assertTrue(isinstance(self.provider, StatisticsProvider), 'Provider initialized')

    @patch.object(requests, 'get')
    def test_get_statistics_from_carto(self, mock_get):
        response_content = get_mocked_data('measurements')
        expected_response = ExternalServiceClientMock.create_response_200(response_content)
        mock_get.return_value = expected_response

        result = self.provider.get_statistics_from_carto()

        self.assertEqual(result, expected_response.json())

    def test_store_in_local_db(self):
        data = {
            'rows': [
                {'station_id': 'aq_alcala_zamora', 'the_geom': '0101000020E61000003DD3CC22D53B0DC048A96A0CB93F4440',
                 'the_geom_webmercator': '0101000020110F0000199D017705D418C1A1369A0CCED65241',
                 'created_at': '2016-11-11T16:18:42Z', 'updated_at': '2017-07-01T09:30:03Z',
                 'measure': 65.3004415547536},
            ],
            'time': 0.499,
            'fields': {'station_id': {'type': 'string', 'pgtype': 'text'},
                       'the_geom': {'type': 'geometry', 'wkbtype': 'Unknown', 'dims': 2, 'srid': 4326},
                       'the_geom_webmercator': {'type': 'geometry', 'wkbtype': 'Unknown', 'dims': 2, 'srid': 3857},
                       'created_at': {'type': 'date', 'pgtype': 'timestamptz'},
                       'updated_at': {'type': 'date', 'pgtype': 'timestamptz'},
                       'measure': {'type': 'number', 'pgtype': 'float8'}}, 'total_rows': 10}
        measure_type = 'AVG'
        start_time = "2016-10-02T01:45:00Z"
        end_time = "2019-10-05T11:00:00Z"

        expected_result = MeasurementsStatistics(id=1, station_id=data['rows'][0]['station_id'],
                                                 the_geom=data['rows'][0]['the_geom'],
                                                 the_geom_webmercator=data['rows'][0]['the_geom_webmercator'],
                                                 created_at=data['rows'][0]['created_at'],
                                                 updated_at=data['rows'][0]['updated_at'],
                                                 measure_type=measure_type, measure=data['rows'][0]['measure'],
                                                 start_time=start_time, end_time=end_time)

        self.provider.store_in_local_db(data, measure_type, start_time, end_time)
        result = MeasurementsStatistics.objects.filter(station_id=data['rows'][0]['station_id'],
                                                       measure_type=measure_type, measure=data['rows'][0]['measure'],
                                                       start_time=start_time, end_time=end_time).first()
        self.assertEqual(result, expected_result)
