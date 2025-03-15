from ddf import G

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from weather.models import City
from weather.models import WeatherRecord


class CurrentWeatherListTestCase(TestCase):
    """Tests for the `CurrentWeatherList` API view."""

    def setUp(self):
        self.client = APIClient()
        # Create test cities
        self.city1 = G(
            City, name="Tokyo", country="Japan", latitude=35.6895, longitude=139.6917
        )
        self.city2 = G(
            City, name="Delhi", country="India", latitude=28.7041, longitude=77.1025
        )
        # Create weather records
        self.record1_old = G(
            WeatherRecord,
            city=self.city1,
            temperature=15.0,
            humidity=55,
            weather_description="cloudy",
        )
        self.record1_new = G(
            WeatherRecord,
            city=self.city1,
            temperature=18.5,
            humidity=60,
            weather_description="clear sky",
        )
        self.record2 = G(
            WeatherRecord,
            city=self.city2,
            temperature=30.0,
            humidity=50,
            weather_description="hot",
        )

    def test_get_current_weather_list(self):
        # Act
        response = self.client.get(reverse("current-weather"))
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        city1_data = next(
            (r for r in response.data if r["city"]["name"] == "Tokyo"), None
        )
        self.assertIsNotNone(city1_data)
        self.assertEqual(city1_data["latest_record"]["temperature"], 18.5)

        city2_data = next(
            (r for r in response.data if r["city"]["name"] == "Delhi"), None
        )
        self.assertIsNotNone(city2_data)
        self.assertEqual(city2_data["latest_record"]["temperature"], 30.0)

    def test_get_current_weather_list_empty(self):
        # Arrange
        WeatherRecord.objects.all().delete()
        # Act
        response = self.client.get(reverse("current-weather"))
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])


class CityWeatherHistoryTestCase(TestCase):
    """Tests for the `CityWeatherHistory` API view."""

    def setUp(self):
        self.client = APIClient()
        self.city = G(
            City, name="Tokyo", country="Japan", latitude=35.6895, longitude=139.6917
        )
        # Create weather records
        self.record1 = G(
            WeatherRecord,
            city=self.city,
            temperature=15.0,
            humidity=55,
            weather_description="cloudy",
        )
        self.record2 = G(
            WeatherRecord,
            city=self.city,
            temperature=20.0,
            humidity=60,
            weather_description="clear sky",
        )

    def test_get_city_weather_history(self):
        # Act
        response = self.client.get(
            reverse("city-weather-history", kwargs={"city_id": self.city.id})
        )
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["temperature"], 20.0)
        self.assertEqual(response.data[1]["temperature"], 15.0)

    def test_get_city_weather_history_no_records(self):
        # Arrange
        WeatherRecord.objects.all().delete()
        # Act
        response = self.client.get(
            reverse("city-weather-history", kwargs={"city_id": self.city.id})
        )
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_get_city_weather_history_city_not_found(self):
        # Act
        response = self.client.get(
            reverse("city-weather-history", kwargs={"city_id": 999})
        )
        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
