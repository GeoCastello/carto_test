import requests
from rest_framework.utils import json

from carto_test.apps.air_quality.models import MeasurementsStatistics
from carto_test.apps.air_quality.providers.assemblers import statistics_query_assembler


class Paths:
    base_path = 'https://aasuero.carto.com:443/api/v2'
    sql = f'{base_path}/sql?q='


class StatisticsProvider:
    def __init__(self, statistics_params: dict):
        self.statistics_params = statistics_params

    @staticmethod
    def store_in_local_db(data: dict):
        for element in data['rows']:
            measurement = MeasurementsStatistics(station_id=element['station_id'],
                                                 the_geom=element['the_geom'],
                                                 the_geom_webmercator=element['the_geom_webmercator'],
                                                 created_at=element['created_at'],
                                                 updated_at=element['updated_at'],
                                                 measure_type=element['measure_type'],
                                                 measure=element['measure'],
                                                 start_time=element['start_time'],
                                                 end_time=element['end_time'],
                                                 population=element['population'])
            measurement.save()

    def get_statistics_from_carto(self) -> json:
        query = statistics_query_assembler(self.statistics_params)
        full_url = Paths.sql + query
        res = requests.get(full_url)

        if 'store' in self.statistics_params.keys() and self.statistics_params['store']:
            self.store_in_local_db(res.json())

        return res.json()
