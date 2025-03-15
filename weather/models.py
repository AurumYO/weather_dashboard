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
