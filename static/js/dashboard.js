document.addEventListener('DOMContentLoaded', () => {
    // Fetch current weather for all cities from GET /api/weather/
    fetch('/api/weather/')
        .then(response => response.json())
        .then(data => {
        const weatherList = document.getElementById('weather-list');
        data.forEach(entry => {
            // Each entry contains a 'city' object and a 'latest_record'
            const { city, latest_record } = entry;
            const createdAt = new Date(latest_record.created_at).toLocaleString();
            const div = document.createElement('div');
            div.classList.add('city-weather');
            div.innerHTML = `
                <h3>${city.name}, ${city.country}</h3>
                <p><strong>Temperature:</strong> ${latest_record.temperature} °C</p>
                <p><strong>Humidity:</strong> ${latest_record.humidity}%</p>
                <p><strong>Description:</strong> ${latest_record.weather_description}</p>
                <p><strong>Updated:</strong> ${createdAt}</p>
            `;
            weatherList.appendChild(div);
        });
    })
    .catch(error => console.error('Error fetching current weather:', error));

    // Fetch historical weather data for a specific city (e.g., city with ID 1)
    fetch('/api/weather/1/')
        .then(response => response.json())
        .then(data => {
            // Sort records by created_at ascending (oldest to newest)
            data.sort((a, b) => new Date(a.created_at) - new Date(b.created_at));
            const labels = data.map(record => new Date(record.created_at).toLocaleTimeString());
            const temperatures = data.map(record => record.temperature);

        // Create a line chart using Chart.js
        const ctx = document.getElementById('tempChart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                label: 'Temperature (°C)',
                data: temperatures,
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                fill: true,
                tension: 0.1,
                }]
            },
            options: {
                responsive: true,
                scales: {
                x: {
                    display: true,
                    title: { display: true, text: 'Time' }
                },
                y: {
                    display: true,
                    title: { display: true, text: 'Temperature (°C)' }
                }
                }
            }
            });
        })
    .catch(error => console.error('Error fetching historical data:', error));
});
