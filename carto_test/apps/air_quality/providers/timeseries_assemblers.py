from rest_framework.utils import json


def query_assembler(statistics_dict: dict) -> json:
    start_time = statistics_dict['start_time'].strftime('%Y-%m-%dT%H:%M:%SZ')
    end_time = statistics_dict['end_time'].strftime('%Y-%m-%dT%H:%M:%SZ')
    query = f"SELECT s.station_id, s.the_geom, s.the_geom_webmercator, s.created_at, s.updated_at, " \
            f"'{statistics_dict['statistical_measurement']}' AS measure_type, " \
            f"{statistics_dict['statistical_measurement']}(m.{statistics_dict['variable']}) AS measure, " \
            f"t.start_time, t.end_time " \
            f"FROM aasuero.test_airquality_measurements m " \
            f"INNER JOIN aasuero.test_airquality_stations s ON m.station_id = s.station_id " \
            f"JOIN (SELECT times AS start_time, lead(times) over (order by times) as end_time " \
            f"FROM generate_series('{start_time}'::timestamp with time zone, " \
            f"'{end_time}'::timestamp with time zone, '{statistics_dict['step']}') times) t " \
            f"ON m.timeinstant BETWEEN t.start_time AND t.end_time " \
            f"GROUP BY s.station_id, s.the_geom, s.the_geom_webmercator, s.created_at, " \
            f"s.updated_at, t.start_time, t.end_time " \
            f"ORDER BY s.station_id, t.start_time"

    return query
