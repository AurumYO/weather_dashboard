import os
import logging
import requests
from celery import shared_task
from typing import Any

from django.conf import settings

from weather.models import City
from weather.models import WeatherRecord


logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
)
def fetch_weather_data(self: Any) -> None:
    """
    Fetch current weather data from OpenWeatherMap for all cities
    and create WeatherRecord instances.

    This task runs asynchronously using Celery and retries up to 5 times in case of failure.

    """
    api_key = settings.OPENWEATHER_API_KEY

    if not api_key:
        logger.error("OPENWEATHER_API_KEY not set in environment variables.")
        return

    base_url = settings.OPENWEATHER_URL

    cities = City.objects.all()
    logger.info("Fetching weather data for %d cities.", cities.count())

    # For each city in our database, fetch the current weather data.
    for city in cities:
        params = {
            "q": city.name,
            "appid": api_key,
            "units": "metric",
        }

        logger.info("Requesting weather data for %s.", city)
        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            data = response.json()

            temperature = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            weather_description = data["weather"][0]["description"]

            # Create a new WeatherRecord
            WeatherRecord.objects.create(
                city=city,
                temperature=temperature,
                humidity=humidity,
                weather_description=weather_description,
            )
            logger.info("Weather data for %s updated successfully.", city)
        else:
            logger.error(
                "Failed to fetch data for %s. Status code: %d - Message: %s",
                city,
                response.status_code,
                response.json().get("message", "Unknown error"),
            )

    logger.info("Completed fetch_weather_data task.")
