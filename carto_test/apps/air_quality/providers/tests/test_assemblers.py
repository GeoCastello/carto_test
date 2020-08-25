from django.test import TestCase

from carto_test.apps.air_quality.providers.statistics_assemblers import query_assembler


class TestAssemblers(TestCase):

    def test_query_assembler(self):
        statistics_request = {
            'start_time': '2016-10-05T11:00:00Z',
            'end_time': '2016-11-11T17:47:17Z',
            'variable': 'co',
            'statistical_measurement': 'AVG'
        }

        expected_result = "SELECT s.station_id, s.the_geom, s.the_geom_webmercator, s.created_at, " \
                          "s.updated_at, AVG(m.co) AS measure " \
                          "FROM aasuero.test_airquality_measurements m " \
                          "INNER JOIN aasuero.test_airquality_stations s ON m.station_id = s.station_id " \
                          "WHERE m.timeinstant BETWEEN '2016-10-05T11:00:00Z'::timestamp with time zone AND " \
                          "'2016-11-11T17:47:17Z'::timestamp with time zone " \
                          "GROUP BY s.station_id, s.the_geom, s.the_geom_webmercator, s.created_at, s.updated_at"
        assembled_query = query_assembler(statistics_request)

        self.assertEqual.__self__.maxDiff = None
        self.assertEqual(assembled_query, expected_result, 'Query assembled')
