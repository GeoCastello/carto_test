from rest_framework import serializers


class StatisticsSerializer(serializers.Serializer):
    POSSIBLE_VARIABLES = ['co', 'no2', 'o3', 'pm10', 'pm2_5', 'so2']
    POSSIBLE_STATISTICS = ['AVG', 'MAX', 'MIN', 'SUM', 'MODE', 'PERCENTILE_CONT', 'PERCENTILE_DISC']
    date_regex = '^((19|20)[0-9][0-9])[-](0[1-9]|1[012])[-](0[1-9]|[12][0-9]|3[01])[T]([01][1-9]|[2][0-3])[:]' \
                 '([0-5][0-9])[:]([0-5][0-9]Z)'

    start_time = serializers.RegexField(regex=date_regex)
    end_time = serializers.RegexField(regex=date_regex)
    variable = serializers.ChoiceField(choices=POSSIBLE_VARIABLES, default='co2')
    statistical_measurement = serializers.ChoiceField(choices=POSSIBLE_STATISTICS, default='avg')
    store = serializers.BooleanField(required=False, default=False)
