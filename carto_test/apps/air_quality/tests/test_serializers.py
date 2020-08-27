from datetime import datetime

import pytz
from django.test import TestCase

from carto_test.apps.air_quality.serializers import StatisticsSerializer, TimeSeriesSerializer


class TestStatisticsSerializer(TestCase):

    def test_serialize(self):
        statistics_request = {
            'start_time': '2016-10-05T11:00:00Z',
            'end_time': '2016-11-11T17:47:17Z',
            'variable': 'co',
            'statistical_measurement': 'AVG',
            'store': False
        }
        expected_result = {
            'start_time': datetime(2016, 10, 5, 11, 0, tzinfo=pytz.utc),
            'end_time': datetime(2016, 11, 11, 17, 47, 17, tzinfo=pytz.utc),
            'variable': 'co',
            'statistical_measurement': 'AVG',
            'store': False
        }

        serialized_statistics_request = StatisticsSerializer(data=statistics_request)
        serialized_statistics_request.is_valid(raise_exception=True)
        validated_data = serialized_statistics_request.validated_data

        self.assertEqual(validated_data['start_time'], expected_result['start_time'])
        self.assertEqual(validated_data['end_time'], expected_result['end_time'])
        self.assertEqual(validated_data['variable'], expected_result['variable'])
        self.assertEqual(validated_data['statistical_measurement'], expected_result['statistical_measurement'])
        self.assertEqual(validated_data['store'], expected_result['store'])


class TestTimeSeriesSerializer(TestCase):

    def test_serialize(self):
        timeseries_request = {
            'start_time': '2016-10-05 11:00:00',
            'end_time': '2016-11-11 17:47:17',
            'variable': 'co',
            'statistical_measurement': 'AVG',
            'step': '1 week',
            'store': False
        }
        expected_result = {
            'start_time': datetime(2016, 10, 5, 11, 0, tzinfo=pytz.utc),
            'end_time': datetime(2016, 11, 11, 17, 47, 17, tzinfo=pytz.utc),
            'variable': 'co',
            'statistical_measurement': 'AVG',
            'step': '1 week',
            'store': False
        }

        serialized_timeseries_request = TimeSeriesSerializer(data=timeseries_request)
        serialized_timeseries_request.is_valid(raise_exception=True)
        validated_data = serialized_timeseries_request.validated_data

        self.assertEqual(validated_data['start_time'], expected_result['start_time'])
        self.assertEqual(validated_data['end_time'], expected_result['end_time'])
        self.assertEqual(validated_data['variable'], expected_result['variable'])
        self.assertEqual(validated_data['statistical_measurement'], expected_result['statistical_measurement'])
        self.assertEqual(validated_data['step'], expected_result['step'])
        self.assertEqual(validated_data['store'], expected_result['store'])
