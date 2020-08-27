import pytz
from rest_framework import serializers

POSSIBLE_VARIABLES = ['co', 'no2', 'o3', 'pm10', 'pm2_5', 'so2']
POSSIBLE_STATISTICS = ['AVG', 'MAX', 'MIN', 'SUM', 'MODE', 'PERCENTILE_CONT', 'PERCENTILE_DISC']


class FilterSerializer(serializers.Serializer):
    stations = serializers.ListField(child=serializers.CharField(), required=False)
    geometries = serializers.ListField(child=serializers.DictField(), required=False)
    geometries_srid = serializers.CharField(required=False, default='4326')


class StatisticsSerializer(serializers.Serializer):
    start_time = serializers.DateTimeField(default_timezone=pytz.utc)
    end_time = serializers.DateTimeField(default_timezone=pytz.utc)
    variable = serializers.ChoiceField(choices=POSSIBLE_VARIABLES, default='co')
    statistical_measurement = serializers.ChoiceField(choices=POSSIBLE_STATISTICS, default='AVG')
    store = serializers.BooleanField(required=False, default=False)
    filters = FilterSerializer(required=False)


class TimeSeriesSerializer(serializers.Serializer):
    POSSIBLE_STEPS = ['1 hour', '1 day', '1 week']
    start_time = serializers.DateTimeField(default_timezone=pytz.utc)
    end_time = serializers.DateTimeField(default_timezone=pytz.utc)
    variable = serializers.ChoiceField(choices=POSSIBLE_VARIABLES, default='co')
    statistical_measurement = serializers.ChoiceField(choices=POSSIBLE_STATISTICS, default='AVG')
    step = serializers.ChoiceField(choices=POSSIBLE_STEPS, default='1 hour')
    store = serializers.BooleanField(required=False, default=False)
    filters = FilterSerializer(required=False)
