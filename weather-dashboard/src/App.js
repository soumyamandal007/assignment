import "./App.css";
import React, { useState } from "react";

function App() {
  const [city, setCity] = useState("");
  const [weather, setWeather] = useState(null);
  const [error, setError] = useState(null);
  const [overview, setOverview] = useState(null);

  const fetchWeather = async () => {
    setError(null);
    try {
      const [currentWeatherResponse, weatherOverviewResponse] =
        await Promise.all([
          fetch(
            `http://127.0.0.1:8000/api/weather/?city=${encodeURIComponent(
              city
            )}`
          ),
          fetch(
            `http://127.0.0.1:8000/api/pollution/?city=${encodeURIComponent(
              city
            )}`
          ),
        ]);

      console.log(currentWeatherResponse, weatherOverviewResponse);

      if (!currentWeatherResponse.ok) {
        throw new Error(
          `City not found or data unavailable: ${currentWeatherResponse.status}`
        );
      }

      if (!weatherOverviewResponse.ok) {
        throw new Error(
          `CIty Data not found: ${weatherOverviewResponse.status}`
        );
      }

      const [currentData, weatherView] = await Promise.all([
        currentWeatherResponse.json(),
        weatherOverviewResponse.json(),
      ]);

      setWeather(currentData);
      setOverview(weatherView);
    } catch (error) {
      console.log(error);
      setError(error.message);
    }
  };

  return (
    <div className="App">
      <div style={{ maxWidth: "800px", margin: "auto" }}>
        <h1>Weather Dashboard</h1>
        <div style={{ display: "flex", marginBottom: "20px" }}>
          <input
            type="text"
            value={city}
            onChange={(e) => setCity(e.target.value)}
            placeholder="Enter city name"
            style={{ flexGrow: 1, marginRight: "10px", padding: "10px" }}
          />
          <button
            onClick={fetchWeather}
            style={{
              padding: "10px 20px",
              backgroundColor: "#007bff",
              color: "white",
              border: "none",
              cursor: "pointer",
            }}
          >
            Get Weather
          </button>
        </div>

        {error && <p style={{ color: "red", textAlign: "center" }}>{error}</p>}
        <h1>Weather Data</h1>
        {weather && (
          <div>
            <h2>City: {weather.city}</h2>
            <p>Temperature: {weather.temperature}°C</p>
            <p>Condition: {weather.condition}</p>
            <p>Description: {weather.description}</p>
          </div>
        )}

        <div>
          <h2>Air Pollution</h2>
          {overview && <h2>Ozone Percentage {overview.pollution}</h2>}
        </div>
      </div>
    </div>
  );
}

export default App;
