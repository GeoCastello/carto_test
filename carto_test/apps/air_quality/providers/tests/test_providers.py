from datetime import datetime
from unittest.mock import patch

import pytz
import requests
from django.test import TestCase

from carto_test.apps.air_quality.models import MeasurementsStatistics, TimeSeries
from carto_test.apps.air_quality.providers.statistics_provider import StatisticsProvider
from carto_test.apps.air_quality.providers.timeseries_provider import TimeSeriesProvider
from carto_test.utils.carto.tests.mocks.carto_services_mock import get_mocked_data
from carto_test.utils.external_service_client.mocks.external_service_client_mock import ExternalServiceClientMock


class TestStatisticsProvider(TestCase):

    def setUp(self):
        self.statistics_request = {
            'start_time': datetime(2016, 10, 5, 11, 0, tzinfo=pytz.utc),
            'end_time': datetime(2016, 11, 11, 17, 47, 17, tzinfo=pytz.utc),
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
                {'station_id': 'aq_alcala_zamora',
                 'the_geom': '0101000020E61000003DD3CC22D53B0DC048A96A0CB93F4440',
                 'the_geom_webmercator': '0101000020110F0000199D017705D418C1A1369A0CCED65241',
                 'created_at': '2016-11-11T16:18:42Z', 'updated_at': '2017-07-01T09:30:03Z',
                 'measure_type': 'AVG', 'measure': 65.3004415547536, 'population': 6929.5869140625,
                 'start_time': '2016-10-02T01:45:00Z', 'end_time': '2019-10-05T11:00:00Z'
                 },
            ],
            'time': 0.499,
            'fields': {'station_id': {'type': 'string', 'pgtype': 'text'},
                       'the_geom': {'type': 'geometry', 'wkbtype': 'Unknown', 'dims': 2,
                                    'srid': 4326},
                       'the_geom_webmercator': {'type': 'geometry', 'wkbtype': 'Unknown', 'dims': 2,
                                                'srid': 3857},
                       'created_at': {'type': 'date', 'pgtype': 'timestamptz'},
                       'updated_at': {'type': 'date', 'pgtype': 'timestamptz'},
                       'measure': {'type': 'number', 'pgtype': 'float8'}}, 'total_rows': 10}

        expected_result = MeasurementsStatistics(id=1, station_id=data['rows'][0]['station_id'],
                                                 the_geom=data['rows'][0]['the_geom'],
                                                 the_geom_webmercator=data['rows'][0][
                                                     'the_geom_webmercator'],
                                                 created_at=data['rows'][0]['created_at'],
                                                 updated_at=data['rows'][0]['updated_at'],
                                                 measure_type=data['rows'][0]['measure_type'],
                                                 measure=data['rows'][0]['measure'],
                                                 population=data['rows'][0]['population'],
                                                 start_time=data['rows'][0]['start_time'],
                                                 end_time=data['rows'][0]['end_time'])

        self.provider.store_in_local_db(data)
        result = MeasurementsStatistics.objects.filter(station_id=data['rows'][0]['station_id'],
                                                       measure_type=data['rows'][0]['measure_type'],
                                                       measure=data['rows'][0]['measure'],
                                                       start_time=data['rows'][0]['start_time'],
                                                       end_time=data['rows'][0]['end_time']).first()
        self.assertEqual(result, expected_result)


class TestTimeSeriesProvider(TestCase):

    def setUp(self):
        self.time_series_request = {
            'start_time': datetime(2016, 10, 5, 11, 0, tzinfo=pytz.utc),
            'end_time': datetime(2016, 11, 11, 17, 47, 17, tzinfo=pytz.utc),
            'variable': 'co',
            'statistical_measurement': 'AVG',
            'step': '1 week'
        }
        self.provider = TimeSeriesProvider(self.time_series_request)

    def test_constructor(self):
        self.assertTrue(isinstance(self.provider, TimeSeriesProvider), 'Provider initialized')

    @patch.object(requests, 'get')
    def test_get_time_series_from_carto(self, mock_get):
        response_content = get_mocked_data('timeseries')
        expected_response = ExternalServiceClientMock.create_response_200(response_content)
        mock_get.return_value = expected_response

        result = self.provider.get_timeseries_from_carto()

        self.assertEqual(result, expected_response.json())

    def test_store_in_local_db(self):
        data = {
            'rows': [
                {'station_id': 'aq_alcala_zamora',
                 'the_geom': '0101000020E61000003DD3CC22D53B0DC048A96A0CB93F4440',
                 'the_geom_webmercator': '0101000020110F0000199D017705D418C1A1369A0CCED65241',
                 'created_at': '2016-11-11T16:18:42Z', 'updated_at': '2017-07-01T09:30:03Z',
                 'measure_type': 'AVG', 'measure': 0.486542900986742,
                 'start_time': '2016-11-05T16:15:00Z', 'end_time': '2016-11-12T16:15:00Z'}
            ],
            'time': 0.212,
            'fields': {'station_id': {'type': 'string', 'pgtype': 'text'},
                       'the_geom': {'type': 'geometry', 'wkbtype': 'Unknown', 'dims': 2,
                                    'srid': 4326},
                       'the_geom_webmercator': {'type': 'geometry', 'wkbtype': 'Unknown', 'dims': 2,
                                                'srid': 3857},
                       'created_at': {'type': 'date', 'pgtype': 'timestamptz'},
                       'updated_at': {'type': 'date', 'pgtype': 'timestamptz'},
                       'measure_type': {'type': 'string', 'pgtype': 'text'},
                       'measure': {'type': 'number', 'pgtype': 'float8'},
                       'start_time': {'type': 'date', 'pgtype': 'timestamptz'},
                       'end_time': {'type': 'date', 'pgtype': 'timestamptz'}},
            'total_rows': 1}

        expected_result = TimeSeries(id=1, station_id=data['rows'][0]['station_id'],
                                     the_geom=data['rows'][0]['the_geom'],
                                     the_geom_webmercator=data['rows'][0]['the_geom_webmercator'],
                                     created_at=data['rows'][0]['created_at'],
                                     updated_at=data['rows'][0]['updated_at'],
                                     measure_type=data['rows'][0]['measure_type'],
                                     measure=data['rows'][0]['measure'],
                                     start_time=data['rows'][0]['start_time'],
                                     end_time=data['rows'][0]['end_time'])

        self.provider.store_in_local_db(data)
        result = TimeSeries.objects.filter(station_id=data['rows'][0]['station_id'],
                                           measure_type=data['rows'][0]['measure_type'],
                                           measure=data['rows'][0]['measure'],
                                           start_time=data['rows'][0]['start_time'],
                                           end_time=data['rows'][0]['end_time']).first()
        self.assertEqual(result, expected_result)
