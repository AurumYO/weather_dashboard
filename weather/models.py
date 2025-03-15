from django.db import models


class City(models.Model):
    """
    Represents a city for which weather data will be recorded.
    """

    name = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        unique_together = ("name", "country")

    def __str__(self):
        return f"{self.name}, {self.country}"


class WeatherRecord(models.Model):
    """
    Represents a weather record for a given city at a specific time.
    """

    city = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name="weather_records"
    )
    temperature = models.FloatField(help_text="Temperature in Celsius")
    humidity = models.PositiveIntegerField(help_text="Humidity percentage")
    weather_description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Weather in {self.city} at {self.created_at}"
