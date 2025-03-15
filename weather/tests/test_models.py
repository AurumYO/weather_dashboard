from django.test import TestCase
from django.db.utils import IntegrityError

from weather.models import City


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
        name_field = City._meta.get_field('name')
        country_field = City._meta.get_field('country')
        # Act & Assert
        self.assertEqual(name_field.max_length, 100)
        self.assertEqual(country_field.max_length, 50)

    def test_query_efficiency(self):
        # Act & Assert
        with self.assertNumQueries(1):
            City.objects.get(name="Tokyo", country="Japan")
