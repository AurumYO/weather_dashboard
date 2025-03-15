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

## API Endpoints Documentation

## 📌 API Documentation with Swagger

This project includes **Swagger UI** for exploring and testing the API.

### 🔹 Access API Documentation

- **Swagger UI:** [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)
- **ReDoc UI:** [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)
- **OpenAPI JSON Schema:** [http://127.0.0.1:8000/swagger.json](http://127.0.0.1:8000/swagger.json)

### 🔹 Install Swagger (If Not Installed)

```bash
poetry install
```

### GET `/api/weather/`

**Description:**
Retrieves a list of all cities along with their latest weather record. This endpoint provides a summary of the current weather conditions for each city in your database.

**Response Format:**

- **city:** Contains the city's details (ID, name, country, latitude, longitude).
- **latest_record:** Contains the latest weather record for the city (temperature, humidity, weather description, and timestamp).

**Example Response:**

```json
[
  {
    "city": {
      "id": 1,
      "name": "Tokyo",
      "country": "Japan",
      "latitude": 35.6895,
      "longitude": 139.6917
    },
    "latest_record": {
      "id": 42,
      "temperature": 30.5,
      "humidity": 60,
      "weather_description": "clear skies",
      "created_at": "2025-03-15T12:34:56Z"
    }
  },
  {
    "city": {
      "id": 2,
      "name": "Delhi",
      "country": "India",
      "latitude": 28.7041,
      "longitude": 77.1025
    },
    "latest_record": {
      "id": 43,
      "temperature": 32.0,
      "humidity": 50,
      "weather_description": "partly cloudy",
      "created_at": "2025-03-15T12:35:01Z"
    }
  }
]
```

### GET `/api/weather/{city_id}/`

**Description:**  
Retrieves all historical weather records for the specified city. This endpoint returns a time-series of weather data, allowing for detailed analysis of past weather conditions for that city.

**Path Parameter:**

- **city(integer):** The unique identifier for the city whose weather history is being requested.

**Response Format:**

Each entry in the response includes the weather record's details (ID, city details, temperature, humidity, weather description, and timestamp).

**Example Response:**

```json
[
  {
    "id": 42,
    "city": {
      "id": 1,
      "name": "Tokyo",
      "country": "Japan",
      "latitude": 35.6895,
      "longitude": 139.6917
    },
    "temperature": 30.5,
    "humidity": 60,
    "weather_description": "clear skies",
    "created_at": "2025-03-15T12:34:56Z"
  },
  {
    "id": 41,
    "city": {
      "id": 1,
      "name": "Tokyo",
      "country": "Japan",
      "latitude": 35.6895,
      "longitude": 139.6917
    },
    "temperature": 29.0,
    "humidity": 65,
    "weather_description": "overcast",
    "created_at": "2025-03-15T11:34:56Z"
  }
]
```
