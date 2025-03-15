from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase
from django.db.utils import IntegrityError

from weather.models import City


class PopulateCitiesCommandTestCase(TestCase):
    """
    Tests for the 'populate_cities' management command.
    """

    def test_command_creates_cities(self):
        # Arrange
        expected_cities = [
            "Tokyo",
            "Delhi",
            "Shanghai",
            "São Paulo",
            "Mexico City",
            "Cairo",
            "Mumbai",
            "Beijing",
            "Dhaka",
            "Osaka",
        ]
        # Act
        call_command("populate_cities")
        # Assert
        self.assertEqual(City.objects.count(), 10)
        for city in expected_cities:
            self.assertTrue(City.objects.filter(name=city).exists())

    def test_command_is_idempotent(self):
        # Act
        call_command("populate_cities")
        call_command("populate_cities")
        # Assert
        self.assertEqual(City.objects.count(), 10)

    @patch("weather.management.commands.populate_cities.logger")
    def test_logging_existing_cities(self, mock_logger):
        # Act
        call_command("populate_cities")
        call_command("populate_cities")
        # Assert
        self.assertTrue(mock_logger.info.called)
        mock_logger.info.assert_any_call("City 'Tokyo, Japan' already exists.")
        mock_logger.info.assert_any_call("City 'Delhi, India' already exists.")

    @patch("weather.models.City.objects.get_or_create")
    @patch("weather.management.commands.populate_cities.logger")
    def test_command_handles_integrity_error(self, mock_logger, mock_get_or_create):
        # Arrange
        mock_get_or_create.side_effect = IntegrityError("Database error")
        # Act
        call_command("populate_cities")
        # Assert
        self.assertTrue(mock_logger.error.called)
        mock_logger.error.assert_any_call(
            "IntegrityError occurred while inserting city 'Tokyo': Database error"
        )

    @patch("weather.models.City.objects.get_or_create")
    @patch("weather.management.commands.populate_cities.logger")
    def test_command_handles_unexpected_error(self, mock_logger, mock_get_or_create):
        # Arrange
        mock_get_or_create.side_effect = Exception("Unexpected failure")
        # Act
        call_command("populate_cities")
        # Assert
        self.assertTrue(mock_logger.error.called)
        mock_logger.error.assert_any_call(
            "Unexpected error while processing city 'Tokyo': Unexpected failure",
            exc_info=True,
        )
