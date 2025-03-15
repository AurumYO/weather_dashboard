from unittest.mock import MagicMock
from unittest.mock import patch
from django.test import TestCase

from weather.models import City
from weather.models import WeatherRecord
from weather.tasks import fetch_weather_data


class FetchWeatherDataTestCase(TestCase):
    """Tests for the `fetch_weather_data` Celery task."""

    def setUp(self):
        self.city1 = City.objects.create(
            name="Tokyo", country="Japan", latitude=35.6895, longitude=139.6917
        )
        self.city2 = City.objects.create(
            name="Delhi", country="India", latitude=28.7041, longitude=77.1025
        )

    @patch("weather.tasks.settings.OPENWEATHER_API_KEY", None)
    @patch("weather.tasks.logger")
    def test_api_key_missing(self, mock_logger):
        # Act
        fetch_weather_data()
        # Assert
        mock_logger.error.assert_called_with(
            "OPENWEATHER_API_KEY not set in environment variables."
        )
        self.assertEqual(WeatherRecord.objects.count(), 0)

    @patch("weather.tasks.requests.get")
    @patch("weather.tasks.settings.OPENWEATHER_API_KEY", "test_api_key")
    @patch(
        "weather.tasks.settings.OPENWEATHER_URL",
        "https://api.openweathermap.org/data/2.5/weather",
    )
    def test_successful_api_call_creates_weather_record(self, mock_get):
        # Arrange & Act
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "main": {"temp": 25.5, "humidity": 60},
            "weather": [{"description": "clear sky"}],
        }
        mock_get.return_value = mock_response

        fetch_weather_data()
        # Assert
        self.assertEqual(WeatherRecord.objects.count(), 2)
        self.assertTrue(
            WeatherRecord.objects.filter(
                city=self.city1, temperature=25.5, humidity=60
            ).exists()
        )
        self.assertTrue(
            WeatherRecord.objects.filter(
                city=self.city2, temperature=25.5, humidity=60
            ).exists()
        )

    @patch("weather.tasks.requests.get")
    @patch("weather.tasks.settings.OPENWEATHER_API_KEY", "test_api_key")
    @patch(
        "weather.tasks.settings.OPENWEATHER_URL",
        "https://api.openweathermap.org/data/2.5/weather",
    )
    @patch("weather.tasks.logger")
    def test_api_failure_logs_error(self, mock_logger, mock_get):
        # Arrange & Act
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "city not found"}
        mock_get.return_value = mock_response

        fetch_weather_data()
        # Assert
        mock_logger.error.assert_any_call(
            "Failed to fetch data for %s. Status code: %d - Message: %s",
            self.city1,
            404,
            "city not found",
        )

        mock_logger.error.assert_any_call(
            "Failed to fetch data for %s. Status code: %d - Message: %s",
            self.city2,
            404,
            "city not found",
        )
        self.assertEqual(
            WeatherRecord.objects.count(), 0
        )

    @patch("weather.tasks.requests.get")
    @patch("weather.tasks.settings.OPENWEATHER_API_KEY", "test_api_key")
    @patch(
        "weather.tasks.settings.OPENWEATHER_URL",
        "https://api.openweathermap.org/data/2.5/weather",
    )
    def test_no_weather_data_does_not_create_record(self, mock_get):
        # Arrange & Act
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"main": {}, "weather": []}
        mock_get.return_value = mock_response
        fetch_weather_data()
        # Assert
        self.assertEqual(WeatherRecord.objects.count(), 0)

    @patch("weather.tasks.requests.get")
    @patch("weather.tasks.settings.OPENWEATHER_API_KEY", "test_api_key")
    @patch(
        "weather.tasks.settings.OPENWEATHER_URL",
        "https://api.openweathermap.org/data/2.5/weather",
    )
    def test_api_called_for_all_cities(self, mock_get):
        # Arrange & Act
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "main": {"temp": 22.0, "humidity": 55},
            "weather": [{"description": "partly cloudy"}],
        }
        mock_get.return_value = mock_response
        fetch_weather_data()
        # Assert
        self.assertEqual(mock_get.call_count, 2)
