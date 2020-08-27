from datetime import datetime

import pytz
from django.test import TestCase

from carto_test.apps.air_quality.providers.assemblers import statistics_query_assembler as statistics_assembler
from carto_test.apps.air_quality.providers.assemblers import timeseries_query_assembler as timeseries_assemblers

geojson = '{"type": "Polygon", ' \
          '"coordinates": [[[-3.63289587199688, 40.56439731247202], ' \
          '[-3.661734983325005, 40.55618117044514], [-3.66310827434063, 40.53583209794804], ' \
          '[-3.6378740519285206, 40.52421992151271], [-3.6148714274168015, 40.5239589506112], ' \
          '[-3.60543005168438, 40.547181381686634], [-3.63289587199688, 40.56439731247202]]]}'


class TestStatisticsAssemblers(TestCase):

    def test_query_assembler_without_filters(self):
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

    def test_query_assembler_with_all_filters(self):
        statistics_request = {
            'start_time': datetime(2016, 10, 5, 11, 0, tzinfo=pytz.utc),
            'end_time': datetime(2016, 11, 11, 17, 47, 17, tzinfo=pytz.utc),
            'variable': 'co',
            'statistical_measurement': 'AVG',
            'filters': {
                'stations': ['station_a', 'station_b', ],
                'geometries': [{"type": "Polygon", "coordinates": [
                    [[-3.63289587199688, 40.56439731247202],
                     [-3.661734983325005, 40.55618117044514],
                     [-3.66310827434063, 40.53583209794804],
                     [-3.6378740519285206, 40.52421992151271],
                     [-3.6148714274168015, 40.5239589506112],
                     [-3.60543005168438, 40.547181381686634],
                     [-3.63289587199688, 40.56439731247202]]]}, ],
                'geometries_srid': '4326'
            }
        }

        expected_result = "SELECT s.station_id, s.the_geom, s.the_geom_webmercator, s.created_at, " \
                          "s.updated_at, 'AVG' AS measure_type, AVG(m.co) AS measure, g.population, " \
                          "'2016-10-05T11:00:00Z' AS start_time, '2016-11-11T17:47:17Z' AS end_time " \
                          "FROM aasuero.test_airquality_measurements m " \
                          "INNER JOIN aasuero.test_airquality_stations s ON m.station_id = s.station_id " \
                          "INNER JOIN aasuero.esp_grid_1km_demographics g " \
                          "ON ST_Intersects(s.the_geom_webmercator, g.the_geom_webmercator) " \
                          "WHERE m.timeinstant BETWEEN '2016-10-05T11:00:00Z'::timestamp with time zone AND " \
                          "'2016-11-11T17:47:17Z'::timestamp with time zone AND " \
                          "s.station_id = 'station_a' OR s.station_id = 'station_b' AND " \
                          f"ST_Intersects(s.the_geom, ST_SetSRID(ST_GeomFromGeoJSON('{geojson}'), 4326)) " \
                          "GROUP BY s.station_id, s.the_geom, s.the_geom_webmercator, s.created_at, " \
                          "s.updated_at, g.population"

        assembled_query = statistics_assembler(statistics_request)

        self.assertEqual.__self__.maxDiff = None
        self.assertEqual(assembled_query, expected_result, 'Query assembled')

    def test_query_assembler_with_only_stations_filters(self):
        statistics_request = {
            'start_time': datetime(2016, 10, 5, 11, 0, tzinfo=pytz.utc),
            'end_time': datetime(2016, 11, 11, 17, 47, 17, tzinfo=pytz.utc),
            'variable': 'co',
            'statistical_measurement': 'AVG',
            'filters': {
                'stations': ['station_a', 'station_b', ]
            }
        }

        expected_result = "SELECT s.station_id, s.the_geom, s.the_geom_webmercator, s.created_at, " \
                          "s.updated_at, 'AVG' AS measure_type, AVG(m.co) AS measure, g.population, " \
                          "'2016-10-05T11:00:00Z' AS start_time, '2016-11-11T17:47:17Z' AS end_time " \
                          "FROM aasuero.test_airquality_measurements m " \
                          "INNER JOIN aasuero.test_airquality_stations s ON m.station_id = s.station_id " \
                          "INNER JOIN aasuero.esp_grid_1km_demographics g " \
                          "ON ST_Intersects(s.the_geom_webmercator, g.the_geom_webmercator) " \
                          "WHERE m.timeinstant BETWEEN '2016-10-05T11:00:00Z'::timestamp with time zone AND " \
                          "'2016-11-11T17:47:17Z'::timestamp with time zone AND " \
                          "s.station_id = 'station_a' OR s.station_id = 'station_b' " \
                          "GROUP BY s.station_id, s.the_geom, s.the_geom_webmercator, s.created_at, " \
                          "s.updated_at, g.population"

        assembled_query = statistics_assembler(statistics_request)

        self.assertEqual.__self__.maxDiff = None
        self.assertEqual(assembled_query, expected_result, 'Query assembled')

    def test_query_assembler_with_only_geometries_filters(self):
        statistics_request = {
            'start_time': datetime(2016, 10, 5, 11, 0, tzinfo=pytz.utc),
            'end_time': datetime(2016, 11, 11, 17, 47, 17, tzinfo=pytz.utc),
            'variable': 'co',
            'statistical_measurement': 'AVG',
            'filters': {
                'geometries': [{"type": "Polygon", "coordinates": [
                    [[-3.63289587199688, 40.56439731247202],
                     [-3.661734983325005, 40.55618117044514],
                     [-3.66310827434063, 40.53583209794804],
                     [-3.6378740519285206, 40.52421992151271],
                     [-3.6148714274168015, 40.5239589506112],
                     [-3.60543005168438, 40.547181381686634],
                     [-3.63289587199688, 40.56439731247202]]]}, ],
                'geometries_srid': '4326'
            }
        }

        expected_result = "SELECT s.station_id, s.the_geom, s.the_geom_webmercator, s.created_at, " \
                          "s.updated_at, 'AVG' AS measure_type, AVG(m.co) AS measure, g.population, " \
                          "'2016-10-05T11:00:00Z' AS start_time, '2016-11-11T17:47:17Z' AS end_time " \
                          "FROM aasuero.test_airquality_measurements m " \
                          "INNER JOIN aasuero.test_airquality_stations s ON m.station_id = s.station_id " \
                          "INNER JOIN aasuero.esp_grid_1km_demographics g " \
                          "ON ST_Intersects(s.the_geom_webmercator, g.the_geom_webmercator) " \
                          "WHERE m.timeinstant BETWEEN '2016-10-05T11:00:00Z'::timestamp with time zone AND " \
                          "'2016-11-11T17:47:17Z'::timestamp with time zone AND " \
                          f"ST_Intersects(s.the_geom, ST_SetSRID(ST_GeomFromGeoJSON('{geojson}'), 4326)) " \
                          "GROUP BY s.station_id, s.the_geom, s.the_geom_webmercator, s.created_at, " \
                          "s.updated_at, g.population"

        assembled_query = statistics_assembler(statistics_request)

        self.assertEqual.__self__.maxDiff = None
        self.assertEqual(assembled_query, expected_result, 'Query assembled')

    def test_query_assembler_with_only_geometries_filters_3857_srid(self):
        statistics_request = {
            'start_time': datetime(2016, 10, 5, 11, 0, tzinfo=pytz.utc),
            'end_time': datetime(2016, 11, 11, 17, 47, 17, tzinfo=pytz.utc),
            'variable': 'co',
            'statistical_measurement': 'AVG',
            'filters': {
                'geometries': [{"type": "Polygon", "coordinates": [
                    [[-3.63289587199688, 40.56439731247202],
                     [-3.661734983325005, 40.55618117044514],
                     [-3.66310827434063, 40.53583209794804],
                     [-3.6378740519285206, 40.52421992151271],
                     [-3.6148714274168015, 40.5239589506112],
                     [-3.60543005168438, 40.547181381686634],
                     [-3.63289587199688, 40.56439731247202]]]}, ],
                'geometries_srid': '3857'
            }
        }

        expected_result = "SELECT s.station_id, s.the_geom, s.the_geom_webmercator, s.created_at, " \
                          "s.updated_at, 'AVG' AS measure_type, AVG(m.co) AS measure, g.population, " \
                          "'2016-10-05T11:00:00Z' AS start_time, '2016-11-11T17:47:17Z' AS end_time " \
                          "FROM aasuero.test_airquality_measurements m " \
                          "INNER JOIN aasuero.test_airquality_stations s ON m.station_id = s.station_id " \
                          "INNER JOIN aasuero.esp_grid_1km_demographics g " \
                          "ON ST_Intersects(s.the_geom_webmercator, g.the_geom_webmercator) " \
                          "WHERE m.timeinstant BETWEEN '2016-10-05T11:00:00Z'::timestamp with time zone AND " \
                          "'2016-11-11T17:47:17Z'::timestamp with time zone AND " \
                          f"ST_Intersects(s.the_geom_webmercator, ST_SetSRID(ST_GeomFromGeoJSON('{geojson}'), 3857)) " \
                          "GROUP BY s.station_id, s.the_geom, s.the_geom_webmercator, s.created_at, " \
                          "s.updated_at, g.population"

        assembled_query = statistics_assembler(statistics_request)

        self.assertEqual.__self__.maxDiff = None
        self.assertEqual(assembled_query, expected_result, 'Query assembled')

    def test_query_assembler_with_only_geometries_filters_another_srid(self):
        statistics_request = {
            'start_time': datetime(2016, 10, 5, 11, 0, tzinfo=pytz.utc),
            'end_time': datetime(2016, 11, 11, 17, 47, 17, tzinfo=pytz.utc),
            'variable': 'co',
            'statistical_measurement': 'AVG',
            'filters': {
                'geometries': [{"type": "Polygon", "coordinates": [
                    [[-3.63289587199688, 40.56439731247202],
                     [-3.661734983325005, 40.55618117044514],
                     [-3.66310827434063, 40.53583209794804],
                     [-3.6378740519285206, 40.52421992151271],
                     [-3.6148714274168015, 40.5239589506112],
                     [-3.60543005168438, 40.547181381686634],
                     [-3.63289587199688, 40.56439731247202]]]}, ],
                'geometries_srid': '32630'
            }
        }

        expected_result = "SELECT s.station_id, s.the_geom, s.the_geom_webmercator, s.created_at, " \
                          "s.updated_at, 'AVG' AS measure_type, AVG(m.co) AS measure, g.population, " \
                          "'2016-10-05T11:00:00Z' AS start_time, '2016-11-11T17:47:17Z' AS end_time " \
                          "FROM aasuero.test_airquality_measurements m " \
                          "INNER JOIN aasuero.test_airquality_stations s ON m.station_id = s.station_id " \
                          "INNER JOIN aasuero.esp_grid_1km_demographics g " \
                          "ON ST_Intersects(s.the_geom_webmercator, g.the_geom_webmercator) " \
                          "WHERE m.timeinstant BETWEEN '2016-10-05T11:00:00Z'::timestamp with time zone AND " \
                          "'2016-11-11T17:47:17Z'::timestamp with time zone AND " \
                          f"ST_Intersects(ST_Transform(s.the_geom, 4326, 32630), " \
                          f"ST_SetSRID(ST_GeomFromGeoJSON('{geojson}'), 32630)) " \
                          "GROUP BY s.station_id, s.the_geom, s.the_geom_webmercator, s.created_at, " \
                          "s.updated_at, g.population"

        assembled_query = statistics_assembler(statistics_request)

        self.assertEqual.__self__.maxDiff = None
        self.assertEqual(assembled_query, expected_result, 'Query assembled')


class TestTimeSeriesAssemblers(TestCase):

    def test_query_assembler_without_filters(self):
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

    def test_query_assembler_with_filters(self):
        timeseries_request = {
            'start_time': datetime(2016, 10, 5, 11, 0, tzinfo=pytz.utc),
            'end_time': datetime(2016, 11, 11, 17, 47, 17, tzinfo=pytz.utc),
            'variable': 'co',
            'statistical_measurement': 'AVG',
            'step': '1 week',
            'filters': {
                'stations': ['station_a', 'station_b', ],
                'geometries': [{"type": "Polygon", "coordinates": [
                    [[-3.63289587199688, 40.56439731247202],
                     [-3.661734983325005, 40.55618117044514],
                     [-3.66310827434063, 40.53583209794804],
                     [-3.6378740519285206, 40.52421992151271],
                     [-3.6148714274168015, 40.5239589506112],
                     [-3.60543005168438, 40.547181381686634],
                     [-3.63289587199688, 40.56439731247202]]]}, ],
                'geometries_srid': '4326'
            }
        }

        expected_result = "SELECT s.station_id, s.the_geom, s.the_geom_webmercator, s.created_at, " \
                          "s.updated_at, 'AVG' AS measure_type, AVG(m.co) AS measure, " \
                          "t.start_time, t.end_time " \
                          "FROM aasuero.test_airquality_measurements m " \
                          "INNER JOIN aasuero.test_airquality_stations s ON m.station_id = s.station_id " \
                          "JOIN (SELECT times AS start_time, lead(times) over (order by times) as end_time " \
                          "FROM generate_series('2016-10-05T11:00:00Z'::timestamp with time zone, " \
                          "'2016-11-11T17:47:17Z'::timestamp with time zone, '1 week') times) t " \
                          "ON m.timeinstant BETWEEN t.start_time AND t.end_time AND " \
                          "s.station_id = 'station_a' OR s.station_id = 'station_b' AND " \
                          f"ST_Intersects(s.the_geom, ST_SetSRID(ST_GeomFromGeoJSON('{geojson}'), 4326)) " \
                          "GROUP BY s.station_id, s.the_geom, s.the_geom_webmercator, s.created_at, " \
                          "s.updated_at, t.start_time, t.end_time " \
                          "ORDER BY s.station_id, t.start_time"

        assembled_query = timeseries_assemblers(timeseries_request)

        self.assertEqual.__self__.maxDiff = None
        self.assertEqual(assembled_query, expected_result, 'Query assembled')

    def test_query_assembler_with_only_stations_filters(self):
        timeseries_request = {
            'start_time': datetime(2016, 10, 5, 11, 0, tzinfo=pytz.utc),
            'end_time': datetime(2016, 11, 11, 17, 47, 17, tzinfo=pytz.utc),
            'variable': 'co',
            'statistical_measurement': 'AVG',
            'step': '1 week',
            'filters': {
                'stations': ['station_a', 'station_b', ]
            }
        }

        expected_result = "SELECT s.station_id, s.the_geom, s.the_geom_webmercator, s.created_at, " \
                          "s.updated_at, 'AVG' AS measure_type, AVG(m.co) AS measure, " \
                          "t.start_time, t.end_time " \
                          "FROM aasuero.test_airquality_measurements m " \
                          "INNER JOIN aasuero.test_airquality_stations s ON m.station_id = s.station_id " \
                          "JOIN (SELECT times AS start_time, lead(times) over (order by times) as end_time " \
                          "FROM generate_series('2016-10-05T11:00:00Z'::timestamp with time zone, " \
                          "'2016-11-11T17:47:17Z'::timestamp with time zone, '1 week') times) t " \
                          "ON m.timeinstant BETWEEN t.start_time AND t.end_time AND " \
                          "s.station_id = 'station_a' OR s.station_id = 'station_b' " \
                          "GROUP BY s.station_id, s.the_geom, s.the_geom_webmercator, s.created_at, " \
                          "s.updated_at, t.start_time, t.end_time " \
                          "ORDER BY s.station_id, t.start_time"

        assembled_query = timeseries_assemblers(timeseries_request)

        self.assertEqual.__self__.maxDiff = None
        self.assertEqual(assembled_query, expected_result, 'Query assembled')

    def test_query_assembler_with_only_geometries_filters(self):
        timeseries_request = {
            'start_time': datetime(2016, 10, 5, 11, 0, tzinfo=pytz.utc),
            'end_time': datetime(2016, 11, 11, 17, 47, 17, tzinfo=pytz.utc),
            'variable': 'co',
            'statistical_measurement': 'AVG',
            'step': '1 week',
            'filters': {
                'geometries': [{"type": "Polygon", "coordinates": [
                    [[-3.63289587199688, 40.56439731247202],
                     [-3.661734983325005, 40.55618117044514],
                     [-3.66310827434063, 40.53583209794804],
                     [-3.6378740519285206, 40.52421992151271],
                     [-3.6148714274168015, 40.5239589506112],
                     [-3.60543005168438, 40.547181381686634],
                     [-3.63289587199688, 40.56439731247202]]]}, ],
                'geometries_srid': '4326'
            }
        }

        expected_result = "SELECT s.station_id, s.the_geom, s.the_geom_webmercator, s.created_at, " \
                          "s.updated_at, 'AVG' AS measure_type, AVG(m.co) AS measure, " \
                          "t.start_time, t.end_time " \
                          "FROM aasuero.test_airquality_measurements m " \
                          "INNER JOIN aasuero.test_airquality_stations s ON m.station_id = s.station_id " \
                          "JOIN (SELECT times AS start_time, lead(times) over (order by times) as end_time " \
                          "FROM generate_series('2016-10-05T11:00:00Z'::timestamp with time zone, " \
                          "'2016-11-11T17:47:17Z'::timestamp with time zone, '1 week') times) t " \
                          "ON m.timeinstant BETWEEN t.start_time AND t.end_time AND " \
                          f"ST_Intersects(s.the_geom, ST_SetSRID(ST_GeomFromGeoJSON('{geojson}'), 4326)) " \
                          "GROUP BY s.station_id, s.the_geom, s.the_geom_webmercator, s.created_at, " \
                          "s.updated_at, t.start_time, t.end_time " \
                          "ORDER BY s.station_id, t.start_time"

        assembled_query = timeseries_assemblers(timeseries_request)

        self.assertEqual.__self__.maxDiff = None
        self.assertEqual(assembled_query, expected_result, 'Query assembled')

    def test_query_assembler_with_only_geometries_filters_3857_srid(self):
        timeseries_request = {
            'start_time': datetime(2016, 10, 5, 11, 0, tzinfo=pytz.utc),
            'end_time': datetime(2016, 11, 11, 17, 47, 17, tzinfo=pytz.utc),
            'variable': 'co',
            'statistical_measurement': 'AVG',
            'step': '1 week',
            'filters': {
                'geometries': [{"type": "Polygon", "coordinates": [
                    [[-3.63289587199688, 40.56439731247202],
                     [-3.661734983325005, 40.55618117044514],
                     [-3.66310827434063, 40.53583209794804],
                     [-3.6378740519285206, 40.52421992151271],
                     [-3.6148714274168015, 40.5239589506112],
                     [-3.60543005168438, 40.547181381686634],
                     [-3.63289587199688, 40.56439731247202]]]}, ],
                'geometries_srid': '3857'
            }
        }

        expected_result = "SELECT s.station_id, s.the_geom, s.the_geom_webmercator, s.created_at, " \
                          "s.updated_at, 'AVG' AS measure_type, AVG(m.co) AS measure, " \
                          "t.start_time, t.end_time " \
                          "FROM aasuero.test_airquality_measurements m " \
                          "INNER JOIN aasuero.test_airquality_stations s ON m.station_id = s.station_id " \
                          "JOIN (SELECT times AS start_time, lead(times) over (order by times) as end_time " \
                          "FROM generate_series('2016-10-05T11:00:00Z'::timestamp with time zone, " \
                          "'2016-11-11T17:47:17Z'::timestamp with time zone, '1 week') times) t " \
                          "ON m.timeinstant BETWEEN t.start_time AND t.end_time AND " \
                          f"ST_Intersects(s.the_geom_webmercator, " \
                          f"ST_SetSRID(ST_GeomFromGeoJSON('{geojson}'), 3857)) " \
                          "GROUP BY s.station_id, s.the_geom, s.the_geom_webmercator, s.created_at, " \
                          "s.updated_at, t.start_time, t.end_time " \
                          "ORDER BY s.station_id, t.start_time"

        assembled_query = timeseries_assemblers(timeseries_request)

        self.assertEqual.__self__.maxDiff = None
        self.assertEqual(assembled_query, expected_result, 'Query assembled')

    def test_query_assembler_with_only_geometries_filters_another_srid(self):
        timeseries_request = {
            'start_time': datetime(2016, 10, 5, 11, 0, tzinfo=pytz.utc),
            'end_time': datetime(2016, 11, 11, 17, 47, 17, tzinfo=pytz.utc),
            'variable': 'co',
            'statistical_measurement': 'AVG',
            'step': '1 week',
            'filters': {
                'geometries': [{"type": "Polygon", "coordinates": [
                    [[-3.63289587199688, 40.56439731247202],
                     [-3.661734983325005, 40.55618117044514],
                     [-3.66310827434063, 40.53583209794804],
                     [-3.6378740519285206, 40.52421992151271],
                     [-3.6148714274168015, 40.5239589506112],
                     [-3.60543005168438, 40.547181381686634],
                     [-3.63289587199688, 40.56439731247202]]]}, ],
                'geometries_srid': '32630'
            }
        }

        expected_result = "SELECT s.station_id, s.the_geom, s.the_geom_webmercator, s.created_at, " \
                          "s.updated_at, 'AVG' AS measure_type, AVG(m.co) AS measure, " \
                          "t.start_time, t.end_time " \
                          "FROM aasuero.test_airquality_measurements m " \
                          "INNER JOIN aasuero.test_airquality_stations s ON m.station_id = s.station_id " \
                          "JOIN (SELECT times AS start_time, lead(times) over (order by times) as end_time " \
                          "FROM generate_series('2016-10-05T11:00:00Z'::timestamp with time zone, " \
                          "'2016-11-11T17:47:17Z'::timestamp with time zone, '1 week') times) t " \
                          "ON m.timeinstant BETWEEN t.start_time AND t.end_time AND " \
                          f"ST_Intersects(ST_Transform(s.the_geom, 4326, 32630), " \
                          f"ST_SetSRID(ST_GeomFromGeoJSON('{geojson}'), 32630)) " \
                          "GROUP BY s.station_id, s.the_geom, s.the_geom_webmercator, s.created_at, " \
                          "s.updated_at, t.start_time, t.end_time " \
                          "ORDER BY s.station_id, t.start_time"

        assembled_query = timeseries_assemblers(timeseries_request)

        self.assertEqual.__self__.maxDiff = None
        self.assertEqual(assembled_query, expected_result, 'Query assembled')
