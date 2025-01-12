import requests
import matplotlib.pyplot as plt
import seaborn as sns

def get_weather(api_key, city):
    """Fetch the weather information for a given city."""
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"  # Use "imperial" for Fahrenheit
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        weather = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"].capitalize(),
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"]
        }

        return weather
    except requests.exceptions.RequestException as e:
        return {"error": f"Unable to fetch weather data: {e}"}
    except KeyError:
        return {"error": "Unexpected response format."}

def visualize_weather_data(weather_data):
    """Create visualizations from weather data."""
    if "error" in weather_data:
        print(weather_data["error"])
        return

    # Data for plotting
    labels = ["Temperature (°C)", "Humidity (%)", "Wind Speed (m/s)"]
    values = [
        weather_data["temperature"],
        weather_data["humidity"],
        weather_data["wind_speed"]
    ]

    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(8, 6))

    # Create a barplot
    ax = sns.barplot(x=labels, y=values, palette="coolwarm")
    ax.set_title(f"Weather Data for {weather_data['city']}", fontsize=16)
    ax.set_ylabel("Values", fontsize=12)

    # Annotate the bars with their values
    for i, v in enumerate(values):
        ax.text(i, v + 0.5, str(v), ha="center", fontsize=10)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    API_KEY = "79858554b362c895483c69eda567abcc"  # Replace with your OpenWeatherMap API key
    city = input("Enter the city name: ")

    weather_info = get_weather(API_KEY, city)

    if "error" in weather_info:
        print(weather_info["error"])
    else:
        print(f"Weather in {weather_info['city']}:\n")
        print(f"Temperature: {weather_info['temperature']}°C")
        print(f"Condition: {weather_info['description']}")
        print(f"Humidity: {weather_info['humidity']}%")
        print(f"Wind Speed: {weather_info['wind_speed']} m/s")

        visualize_weather_data(weather_info)
