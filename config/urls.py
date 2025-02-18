"""carto_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from rest_framework import routers

from carto_test.apps.air_quality import views as air_quality_views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'air_quality', air_quality_views.AirQualityViewSet, basename='air_quality')

urlpatterns = [
    url(r'^', include(router.urls)),
]
