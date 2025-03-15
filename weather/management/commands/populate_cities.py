from typing import Any
from logging import getLogger

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from weather.models import City

logger = getLogger(__name__)


class Command(BaseCommand):
    help = "Populates the database with the 10 largest cities in the world for weather tracking."

    def handle(self, *args: tuple[Any, ...], **options: dict[str, Any]) -> None:
        cities_data: list[dict[str, Any]] = [
            {
                "name": "Tokyo",
                "country": "Japan",
                "latitude": 35.6895,
                "longitude": 139.6917,
            },
            {
                "name": "Delhi",
                "country": "India",
                "latitude": 28.7041,
                "longitude": 77.1025,
            },
            {
                "name": "Shanghai",
                "country": "China",
                "latitude": 31.2304,
                "longitude": 121.4737,
            },
            {
                "name": "São Paulo",
                "country": "Brazil",
                "latitude": -23.5505,
                "longitude": -46.6333,
            },
            {
                "name": "Mexico City",
                "country": "Mexico",
                "latitude": 19.4326,
                "longitude": -99.1332,
            },
            {
                "name": "Cairo",
                "country": "Egypt",
                "latitude": 30.0444,
                "longitude": 31.2357,
            },
            {
                "name": "Mumbai",
                "country": "India",
                "latitude": 19.0760,
                "longitude": 72.8777,
            },
            {
                "name": "Beijing",
                "country": "China",
                "latitude": 39.9042,
                "longitude": 116.4074,
            },
            {
                "name": "Dhaka",
                "country": "Bangladesh",
                "latitude": 23.8103,
                "longitude": 90.4125,
            },
            {
                "name": "Osaka",
                "country": "Japan",
                "latitude": 34.6937,
                "longitude": 135.5023,
            },
        ]

        for city_data in cities_data:
            try:
                city, created = City.objects.get_or_create(
                    name=city_data["name"],
                    country=city_data["country"],
                    defaults={
                        "latitude": city_data["latitude"],
                        "longitude": city_data["longitude"],
                    },
                )
                if created:
                    logger.info(f"City '{city}' created successfully.")
                else:
                    logger.info(f"City '{city}' already exists.")
            except IntegrityError as e:
                logger.error(
                    f"IntegrityError occurred while inserting city '{city_data['name']}': {e}"
                )
            except Exception as e:
                logger.error(
                    f"Unexpected error while processing city '{city_data['name']}': {e}",
                    exc_info=True,
                )
