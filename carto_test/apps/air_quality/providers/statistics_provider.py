import requests
from rest_framework.utils import json

from carto_test.apps.air_quality.models import MeasurementsStatistics
from carto_test.apps.air_quality.providers.statistics_assemblers import query_assembler
from carto_test.utils.external_service_client.external_service_client import ExternalServiceClient


class Paths:
    base_path = 'https://aasuero.carto.com:443/api/v2'
    sql = f'{base_path}/sql?q='


class StatisticsProvider:
    def __init__(self, statistics_request: dict):
        self.statistics_request = statistics_request
        self.client = ExternalServiceClient(Paths.base_path, map_exceptions=True)

    @staticmethod
    def store_in_local_db(data: dict, measure_type: str, start_time: str, end_time: str):
        for element in data['rows']:
            measurement = MeasurementsStatistics(station_id=element['station_id'], the_geom=element['the_geom'],
                                                 the_geom_webmercator=element['the_geom_webmercator'],
                                                 created_at=element['created_at'], updated_at=element['updated_at'],
                                                 measure_type=measure_type, measure=element['measure'],
                                                 start_time=start_time, end_time=end_time)
            measurement.save()

    def get_statistics_from_carto(self) -> json:
        query = query_assembler(self.statistics_request)
        full_url = Paths.sql + query
        res = requests.get(full_url)

        if 'store' in self.statistics_request.keys() and self.statistics_request['store']:
            measure_type = self.statistics_request['statistical_measurement']
            start_time = self.statistics_request['start_time']
            end_time = self.statistics_request['end_time']
            self.store_in_local_db(res.json(), measure_type, start_time, end_time)

        return res.json()
