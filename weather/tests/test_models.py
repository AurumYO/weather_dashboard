import datetime
from ddf import G

from django.test import TestCase
from django.db.utils import IntegrityError
from django.utils import timezone

from weather.models import City
from weather.models import WeatherRecord


class CityModelTest(TestCase):
    def setUp(self):
        self.city = City.objects.create(
            name="Tokyo",
            country="Japan",
            latitude=35.6895,
            longitude=139.6917,
        )

    def test_model_str_method(self):
        # Arrange
        expected_str = "Tokyo, Japan"
        # Act & Assert
        self.assertEqual(str(self.city), expected_str)

    def test_unique_together_constraint(self):
        # Act & Assert
        with self.assertRaises(IntegrityError):
            City.objects.create(
                name="Tokyo",
                country="Japan",
                latitude=35.6895,
                longitude=139.6917,
            )

    def test_field_max_lengths(self):
        # Arrange
        name_field = City._meta.get_field("name")
        country_field = City._meta.get_field("country")
        # Act & Assert
        self.assertEqual(name_field.max_length, 100)
        self.assertEqual(country_field.max_length, 50)

    def test_query_efficiency(self):
        # Act & Assert
        with self.assertNumQueries(1):
            City.objects.get(name="Tokyo", country="Japan")


class WeatherRecordModelTest(TestCase):
    def setUp(self):
        self.city = G(
            City,
            name="Tokyo",
            country="Japan",
            latitude=35.6895,
            longitude=139.6917,
        )
        self.weather_record = WeatherRecord.objects.create(
            city=self.city,
            temperature=30.5,
            humidity=60,
            weather_description="Clear skies",
        )

    def test_weather_model_record_str(self):
        # Arrange
        expected = f"Weather in {self.city} at {self.weather_record.created_at}"
        # Act & Assert
        self.assertEqual(str(self.weather_record), expected)

    def test_weather_record_field_values(self):
        # Assert
        self.assertEqual(self.weather_record.city, self.city)
        self.assertEqual(self.weather_record.temperature, 30.5)
        self.assertEqual(self.weather_record.humidity, 60)
        self.assertEqual(self.weather_record.weather_description, "Clear skies")

    def test_created_at_auto_set(self):
        # Act & Aseert
        self.assertIsNotNone(self.weather_record.created_at)
        now = timezone.now()
        self.assertTrue(
            now - self.weather_record.created_at < datetime.timedelta(seconds=5)
        )

    def test_query_efficiency(self):
        # Act & Aseert
        with self.assertNumQueries(1):
            record = WeatherRecord.objects.get(id=self.weather_record.id)
            _ = record.weather_description
