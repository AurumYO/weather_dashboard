from ddf import G
from django.test import TestCase

from weather.models import City
from weather.models import WeatherRecord
from weather.serializers import CitySerializer
from weather.serializers import WeatherRecordSerializer


class CitySerializerTestCase(TestCase):
    """Test case for the CitySerializer."""

    def setUp(self):
        # Set up test data
        self.city = G(
            City,
            name="Tokyo",
            country="Japan",
            latitude=35.6895,
            longitude=139.6917,
        )
        self.data = {
            "name": "Delhi",
            "country": "India",
            "latitude": 28.7041,
            "longitude": 77.1025,
        }

    def test_city_serializer_serialization(self):
        # Arrange
        expected_data = {
            "id": self.city.id,
            "name": "Tokyo",
            "country": "Japan",
            "latitude": 35.6895,
            "longitude": 139.6917,
        }
        # Act
        serializer = CitySerializer(instance=self.city)
        # Assert
        self.assertEqual(serializer.data, expected_data)

    def test_city_serializer_deserialization_valid(self):
        # Act
        serializer = CitySerializer(data=self.data)
        # Assert
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_city_serializer_deserialization_invalid(self):
        # Arrange
        data = {"name": "Delhi"}
        # Act
        serializer = CitySerializer(data=data)
        # Assert
        self.assertFalse(serializer.is_valid())
        self.assertIn("country", serializer.errors)
        self.assertIn("latitude", serializer.errors)
        self.assertIn("longitude", serializer.errors)


class WeatherRecordSerializerTestCase(TestCase):
    """Test case for the WeatherRecordSerializer."""

    def setUp(self):
        # Set up test data
        self.city = G(
            City,
            name="Tokyo",
            country="Japan",
            latitude=35.6895,
            longitude=139.6917,
        )
        self.weather_record = G(
            WeatherRecord,
            city=self.city,
            temperature=20.5,
            humidity=60,
            weather_description="clear sky",
        )

    def test_weather_record_serializer_serialization(self):
        # Arrange
        serializer = WeatherRecordSerializer(instance=self.weather_record)
        expected_data = {
            "id": self.weather_record.id,
            "city": {
                "id": self.city.id,
                "name": "Tokyo",
                "country": "Japan",
                "latitude": 35.6895,
                "longitude": 139.6917,
            },
            "temperature": 20.5,
            "humidity": 60,
            "weather_description": "clear sky",
            "created_at": serializer.data["created_at"],
        }
        # Assert
        self.assertEqual(serializer.data, expected_data)

    def test_weather_record_serializer_readonly_city(self):
        # Arrange
        data = {
            "city": {
                "id": self.city.id,
                "name": "New York",
                "country": "USA",
                "latitude": 40.7128,
                "longitude": -74.0060,
            },
            "temperature": 15.0,
            "humidity": 50,
            "weather_description": "partly cloudy",
        }
        # Act
        serializer = WeatherRecordSerializer(data=data)
        # Assert
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertNotIn("city", serializer.validated_data)

    def test_weather_record_serializer_missing_fields(self):
        # Arrange
        data = {"temperature": 25.0}
        # Act
        serializer = WeatherRecordSerializer(data=data)
        # Assert
        self.assertFalse(serializer.is_valid())
        self.assertIn("humidity", serializer.errors)
        self.assertIn("weather_description", serializer.errors)
