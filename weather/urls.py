from django.urls import path

from weather.views import CityWeatherHistory
from weather.views import CurrentWeatherList


urlpatterns = [
    path("weather/", CurrentWeatherList.as_view(), name="current-weather"),
    path(
        "weather/<int:city_id>/",
        CityWeatherHistory.as_view(),
        name="city-weather-history",
    ),
]
