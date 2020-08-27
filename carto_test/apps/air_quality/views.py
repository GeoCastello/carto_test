from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from carto_test.apps.air_quality.providers.statistics_provider import StatisticsProvider
from carto_test.apps.air_quality.providers.timeseries_provider import TimeSeriesProvider
from carto_test.apps.air_quality.serializers import StatisticsSerializer, TimeSeriesSerializer


class AirQualityViewSet(ViewSet):

    @action(methods=['post'], detail=False, url_path='statistics')
    def statistics(self, request):
        serializer = StatisticsSerializer(data=request.data['params'])
        serializer.is_valid(raise_exception=True)
        provider = StatisticsProvider(serializer.validated_data)
        response = provider.get_statistics_from_carto()

        return Response(response, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='timeseries')
    def time_series(self, request):
        serializer = TimeSeriesSerializer(data=request.data['params'])
        serializer.is_valid(raise_exception=True)
        provider = TimeSeriesProvider(serializer.validated_data)
        response = provider.get_timeseries_from_carto()

        return Response(response, status=status.HTTP_200_OK)
