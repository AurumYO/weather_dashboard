from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from django.shortcuts import get_object_or_404

from weather.models import City
from weather.models import WeatherRecord
from weather.serializers import CitySerializer
from weather.serializers import WeatherRecordSerializer


class CurrentWeatherList(APIView):
    """
    Retrieve current weather data for all cities.
    Returns the latest WeatherRecord for each city.
    """

    def get(self, request, format=None):
        cities = City.objects.all()
        results = []
        for city in cities:
            latest_record = city.weather_records.order_by("-created_at").first()
            if latest_record:
                results.append(
                    {
                        "city": CitySerializer(city).data,
                        "latest_record": WeatherRecordSerializer(latest_record).data,
                    }
                )

        return Response(results)


class CityWeatherHistory(generics.ListAPIView):
    """
    Retrieve detailed historical weather data for a specific city.
    """

    serializer_class = WeatherRecordSerializer

    def get_queryset(self):
        city_id = self.kwargs.get("city_id")
        # Ensure the city exists; returns 404 if not found.
        city = get_object_or_404(City, id=city_id)

        return city.weather_records.order_by("-created_at")
