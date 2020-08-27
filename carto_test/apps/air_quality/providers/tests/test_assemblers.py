from datetime import datetime

import pytz
from django.test import TestCase

from carto_test.apps.air_quality.providers.statistics_assemblers import query_assembler as statistics_assembler
from carto_test.apps.air_quality.providers.timeseries_assemblers import query_assembler as timeseries_assemblers


class TestStatisticsAssemblers(TestCase):

    def test_query_assembler(self):
        statistics_request = {
            'start_time': datetime(2016, 10, 5, 11, 0, tzinfo=pytz.utc),
            'end_time': datetime(2016, 11, 11, 17, 47, 17, tzinfo=pytz.utc),
            'variable': 'co',
            'statistical_measurement': 'AVG'
        }

        expected_result = "SELECT s.station_id, s.the_geom, s.the_geom_webmercator, s.created_at, " \
                          "s.updated_at, 'AVG' AS measure_type, AVG(m.co) AS measure, g.population, " \
                          "'2016-10-05T11:00:00Z' AS start_time, '2016-11-11T17:47:17Z' AS end_time " \
                          "FROM aasuero.test_airquality_measurements m " \
                          "INNER JOIN aasuero.test_airquality_stations s ON m.station_id = s.station_id " \
                          "INNER JOIN aasuero.esp_grid_1km_demographics g " \
                          "ON ST_Intersects(s.the_geom_webmercator, g.the_geom_webmercator) " \
                          "WHERE m.timeinstant BETWEEN '2016-10-05T11:00:00Z'::timestamp with time zone AND " \
                          "'2016-11-11T17:47:17Z'::timestamp with time zone " \
                          "GROUP BY s.station_id, s.the_geom, s.the_geom_webmercator, s.created_at, " \
                          "s.updated_at, g.population"
        assembled_query = statistics_assembler(statistics_request)

        self.assertEqual.__self__.maxDiff = None
        self.assertEqual(assembled_query, expected_result, 'Query assembled')


class TestTimweSeriesAssemblers(TestCase):

    def test_query_assembler(self):
        timeseries_request = {
            'start_time': datetime(2016, 10, 5, 11, 0, tzinfo=pytz.utc),
            'end_time': datetime(2016, 11, 11, 17, 47, 17, tzinfo=pytz.utc),
            'variable': 'co',
            'statistical_measurement': 'AVG',
            'step': '1 week'
        }

        expected_result = "SELECT s.station_id, s.the_geom, s.the_geom_webmercator, s.created_at, " \
                          "s.updated_at, 'AVG' AS measure_type, AVG(m.co) AS measure, " \
                          "t.start_time, t.end_time " \
                          "FROM aasuero.test_airquality_measurements m " \
                          "INNER JOIN aasuero.test_airquality_stations s ON m.station_id = s.station_id " \
                          "JOIN (SELECT times AS start_time, lead(times) over (order by times) as end_time " \
                          "FROM generate_series('2016-10-05T11:00:00Z'::timestamp with time zone, " \
                          "'2016-11-11T17:47:17Z'::timestamp with time zone, '1 week') times) t " \
                          "ON m.timeinstant BETWEEN t.start_time AND t.end_time " \
                          "GROUP BY s.station_id, s.the_geom, s.the_geom_webmercator, s.created_at, " \
                          "s.updated_at, t.start_time, t.end_time " \
                          "ORDER BY s.station_id, t.start_time"

        assembled_query = timeseries_assemblers(timeseries_request)

        self.assertEqual.__self__.maxDiff = None
        self.assertEqual(assembled_query, expected_result, 'Query assembled')
