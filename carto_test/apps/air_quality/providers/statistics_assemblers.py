from rest_framework.utils import json


def query_assembler(statistics_dict: dict) -> json:
    query = f"SELECT s.station_id, s.the_geom, s.the_geom_webmercator, s.created_at, s.updated_at, " \
            f"'{statistics_dict['statistical_measurement']}' AS measure_type, " \
            f"{statistics_dict['statistical_measurement']}(m.{statistics_dict['variable']}) AS measure, " \
            f"g.population, '{statistics_dict['start_time']}' AS start_time, " \
            f"'{statistics_dict['end_time']}' AS end_time " \
            f"FROM aasuero.test_airquality_measurements m " \
            f"INNER JOIN aasuero.test_airquality_stations s ON m.station_id = s.station_id " \
            f"INNER JOIN aasuero.esp_grid_1km_demographics g " \
            f"ON ST_Intersects(s.the_geom_webmercator, g.the_geom_webmercator) " \
            f"WHERE m.timeinstant BETWEEN '{statistics_dict['start_time']}'::timestamp with time zone AND " \
            f"'{statistics_dict['end_time']}'::timestamp with time zone " \
            f"GROUP BY s.station_id, s.the_geom, s.the_geom_webmercator, s.created_at, " \
            f"s.updated_at, g.population"

    return query
