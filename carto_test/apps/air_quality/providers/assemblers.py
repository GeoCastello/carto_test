from rest_framework.utils import json


def get_geometry_field(srid):
    if srid == '4326':
        geom_field = 's.the_geom'
    elif srid == '3857':
        geom_field = 's.the_geom_webmercator'
    else:
        geom_field = f'ST_Transform(s.the_geom, 4326, {srid})'

    return geom_field


def get_stations_where(stations):
    stations_where = f"AND s.station_id = '{stations[0]}' "
    for i in range(1, len(stations)):
        stations_where += f"OR s.station_id = '{stations[i]}' "

    return stations_where


def get_geometries_where(geometries, geom_field, geometries_srid):
    geometries_where = ''
    for geometry in geometries:
        geometry_json = json.dumps(geometry)
        geom = f"ST_GeomFromGeoJSON('{geometry_json}')"
        geometries_where += f'AND ST_Intersects({geom_field}, ' \
                            f'ST_SetSRID({geom}, {geometries_srid})) '

    return geometries_where


def complete_q_where_with_filters(filters, q_where):
    stations = filters.get('stations', None)
    geometries = filters.get('geometries', None)
    geometries_srid = filters.get('geometries_srid')

    if stations is not None and stations != []:
        stations_where = get_stations_where(stations)
        q_where += stations_where

    if geometries is not None:
        geom_field = get_geometry_field(geometries_srid)
        geometries_where = get_geometries_where(geometries, geom_field, geometries_srid)
        q_where += geometries_where

    return q_where


def statistics_query_assembler(statistics_dict: dict) -> json:
    start_time = statistics_dict['start_time'].strftime('%Y-%m-%dT%H:%M:%SZ')
    end_time = statistics_dict['end_time'].strftime('%Y-%m-%dT%H:%M:%SZ')
    filters = statistics_dict.get('filters', None)

    q_select = f"SELECT s.station_id, s.the_geom, s.the_geom_webmercator, s.created_at, " \
               f"s.updated_at, '{statistics_dict['statistical_measurement']}' AS measure_type, " \
               f"{statistics_dict['statistical_measurement']}(m.{statistics_dict['variable']}) AS measure, " \
               f"g.population, '{start_time}' AS start_time, '{end_time}' AS end_time "

    q_from = "FROM aasuero.test_airquality_measurements m "

    q_joins = "INNER JOIN aasuero.test_airquality_stations s ON m.station_id = s.station_id " \
              "INNER JOIN aasuero.esp_grid_1km_demographics g " \
              "ON ST_Intersects(s.the_geom_webmercator, g.the_geom_webmercator) "

    q_where = f"WHERE m.timeinstant BETWEEN '{start_time}'::timestamp with time zone AND " \
              f"'{end_time}'::timestamp with time zone "

    q_group_by = "GROUP BY s.station_id, s.the_geom, s.the_geom_webmercator, s.created_at, " \
                 "s.updated_at, g.population"

    if filters is not None:
        q_where = complete_q_where_with_filters(filters, q_where)

    query = q_select + q_from + q_joins + q_where + q_group_by

    return query


def timeseries_query_assembler(statistics_dict: dict) -> json:
    start_time = statistics_dict['start_time'].strftime('%Y-%m-%dT%H:%M:%SZ')
    end_time = statistics_dict['end_time'].strftime('%Y-%m-%dT%H:%M:%SZ')
    filters = statistics_dict.get('filters', None)
    q_select = f"SELECT s.station_id, s.the_geom, s.the_geom_webmercator, s.created_at, " \
               f"s.updated_at, '{statistics_dict['statistical_measurement']}' AS measure_type, " \
               f"{statistics_dict['statistical_measurement']}(m.{statistics_dict['variable']}) AS measure, " \
               f"t.start_time, t.end_time "

    q_from = "FROM aasuero.test_airquality_measurements m "

    q_joins = f"INNER JOIN aasuero.test_airquality_stations s ON m.station_id = s.station_id " \
              f"JOIN (SELECT times AS start_time, lead(times) over (order by times) as end_time " \
              f"FROM generate_series('{start_time}'::timestamp with time zone, " \
              f"'{end_time}'::timestamp with time zone, '{statistics_dict['step']}') times) t " \
              f"ON m.timeinstant BETWEEN t.start_time AND t.end_time "

    q_group_by = "GROUP BY s.station_id, s.the_geom, s.the_geom_webmercator, s.created_at, " \
                 "s.updated_at, t.start_time, t.end_time "

    q_order_by = "ORDER BY s.station_id, t.start_time"

    if filters is not None:
        q_where = complete_q_where_with_filters(filters, '')

        query = q_select + q_from + q_joins + q_where + q_group_by + q_order_by
    else:
        query = q_select + q_from + q_joins + q_group_by + q_order_by

    return query
