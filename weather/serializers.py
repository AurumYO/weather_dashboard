from rest_framework import serializers

from weather.models import City
from weather.models import WeatherRecord


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ["id", "name", "country", "latitude", "longitude"]


class WeatherRecordSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)

    class Meta:
        model = WeatherRecord
        fields = [
            "id",
            "city",
            "temperature",
            "humidity",
            "weather_description",
            "created_at",
        ]
