from unittest.mock import patch

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from carto_test.apps.air_quality.providers.statistics_provider import StatisticsProvider
from carto_test.apps.air_quality.providers.timeseries_provider import TimeSeriesProvider
from carto_test.utils.carto.tests.mocks.carto_services_mock import get_mocked_data


class TestAirQualityViews(TestCase):
    def setUp(self):
        self.client = APIClient()

    @patch.object(StatisticsProvider, 'get_statistics_from_carto')
    def test_statistics_response_200_and_correct_content(self, mock_get):
        expected_response = get_mocked_data('measurements')
        mock_get.return_value = expected_response
        params = {
            'params': {
                'start_time': '2016-10-05T11:00:00Z',
                'end_time': '2016-11-11T17:47:17Z',
                'variable': 'co',
                'statistical_measurement': 'AVG',
                'store': False
            }
        }
        response = self.client.post('/air_quality/statistics', data=params, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.json(), expected_response)

    def test_statistics_response_400_when_date_has_incorrect_format(self):
        params = {
            'params': {
                'start_time': '2016-10-05',
                'end_time': '2016-11-11T17:47:17Z',
                'variable': 'co',
                'statistical_measurement': 'AVG',
                'store': False
            }
        }
        response = self.client.post('/air_quality/statistics', data=params, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_statistics_response_400_when_variable_does_not_exists(self):
        params = {
            'params': {
                'start_time': '2016-10-05T11:00:00Z',
                'end_time': '2016-11-11T17:47:17Z',
                'variable': 'wrong_variable',
                'statistical_measurement': 'AVG',
                'store': False
            }
        }
        response = self.client.post('/air_quality/statistics', data=params, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_statistics_response_400_when_statistical_measurement_does_not_exists(self):
        params = {
            'params': {
                'start_time': '2016-10-05T11:00:00Z',
                'end_time': '2016-11-11T17:47:17Z',
                'variable': 'co',
                'statistical_measurement': 'wrong_measurement',
                'store': False
            }
        }
        response = self.client.post('/air_quality/statistics', data=params, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch.object(StatisticsProvider, 'get_statistics_from_carto')
    def test_statistics_response_200_when_store_not_provided(self, mock_get):
        expected_response = get_mocked_data('measurements')
        mock_get.return_value = expected_response
        params = {
            'params': {
                'start_time': '2016-10-05T11:00:00Z',
                'end_time': '2016-11-11T17:47:17Z',
                'variable': 'co',
                'statistical_measurement': 'AVG'
            }
        }
        response = self.client.post('/air_quality/statistics', data=params, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.json(), expected_response)

    @patch.object(TimeSeriesProvider, 'get_timeseries_from_carto')
    def test_time_series_response_200_and_correct_content(self, mock_get):
        expected_response = get_mocked_data('timeseries')
        mock_get.return_value = expected_response
        params = {
            'params': {
                'start_time': '2016-11-05T16:15:00Z',
                'end_time': '2016-11-26T16:15:00Z',
                'variable': 'co',
                'statistical_measurement': 'AVG',
                'step': '1 week',
                'store': False
            }
        }
        response = self.client.post('/air_quality/timeseries', data=params, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.json(), expected_response)

    def test_time_series_response_400_when_date_has_incorrect_format(self):
        params = {
            'params': {
                'start_time': '2016-11-05',
                'end_time': '2016-11-26T16:15:00Z',
                'variable': 'co',
                'statistical_measurement': 'AVG',
                'step': '1 week',
                'store': False
            }
        }
        response = self.client.post('/air_quality/timeseries', data=params, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_time_series_response_400_when_variable_does_not_exists(self):
        params = {
            'params': {
                'start_time': '2016-10-05T11:00:00Z',
                'end_time': '2016-11-11T17:47:17Z',
                'variable': 'wrong_variable',
                'statistical_measurement': 'AVG',
                'step': '1 week',
                'store': False
            }
        }
        response = self.client.post('/air_quality/timeseries', data=params, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_time_series_response_400_when_statistical_measurement_does_not_exists(self):
        params = {
            'params': {
                'start_time': '2016-10-05T11:00:00Z',
                'end_time': '2016-11-11T17:47:17Z',
                'variable': 'co',
                'statistical_measurement': 'wrong_measurement',
                'step': '1 week',
                'store': False
            }
        }
        response = self.client.post('/air_quality/timeseries', data=params, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_time_series_response_400_when_step_does_not_exists(self):
        params = {
            'params': {
                'start_time': '2016-10-05T11:00:00Z',
                'end_time': '2016-11-11T17:47:17Z',
                'variable': 'co',
                'statistical_measurement': 'wrong_measurement',
                'step': '1 month',
                'store': False
            }
        }
        response = self.client.post('/air_quality/timeseries', data=params, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
