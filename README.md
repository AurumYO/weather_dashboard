# Weather Dashboard Project

## Populating CityWeather Data

To populate the City model with City data from the populate_cities.py, use the following command:

```bash
poetry run python manage.py populate_cities
```

Command Description

- This command creates Cities data for the 10 largest cities in the world.
- Those cities will be used to fech weather data for from OPenWeather API.
- The data includes citi name, country, latitude, and longitude.

Preconditions

Before running the command, ensure:

Database is set up and migrations are applied:

```bash
poetry run python manage.py migrate
```

Environment variables are set (if required for the API key).
