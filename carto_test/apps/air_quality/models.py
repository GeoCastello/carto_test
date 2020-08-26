from django.contrib.gis.db import models


class MeasurementsStatistics(models.Model):
    station_id = models.CharField(max_length=50)
    the_geom = models.PointField(srid=4326)
    the_geom_webmercator = models.PointField(srid=3857)
    created_at = models.CharField(max_length=30)
    updated_at = models.CharField(max_length=30)
    measure_type = models.CharField(max_length=10)
    measure = models.FloatField()
    start_time = models.CharField(max_length=30)
    end_time = models.CharField(max_length=30)
    population = models.FloatField(null=True)
