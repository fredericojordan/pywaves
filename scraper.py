import datetime
import os

import requests
from dotenv import load_dotenv

load_dotenv()


OPENWEATHER_APP_ID = os.getenv("OPENWEATHER_APP_ID")
OPENWEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5"
OPENWEATHER_FLORIANOPOLIS_ID = "3463237"

DARKSKY_SECRET_KEY = os.getenv("DARKSKY_SECRET_KEY")
DARKSKY_BASE_URL = "https://api.darksky.net/forecast"

STORMGLASS_API_KEY = os.getenv("STORMGLASS_API_KEY")
STORMGLASS_BASE_URL = "https://api.stormglass.io/v1/weather/point"


def print_weather(json_data):
    title = f"OpenWeather weather for {json_data['name']}:"
    print("-" * len(title))
    print(title)
    print("-" * len(title))

    print(f"Timestamp:   {json_data['timestamp']}")
    print(f"Weather:     {json_data['description']}")
    print(
        f"Temperature: {json_data['temp']} °C ({json_data['temp_min']}-{json_data['temp_max']})"
    )
    print(f"Humidity:    {json_data['humidity']} %")
    print(f"Wind speed:  {json_data['wind_speed']} m/s")
    print(f"Cloud cover: {json_data['cloud_coverage']} %")
    print("-" * len(title))


def parse_openweather_weather(json_data):
    return {
        "name": f"{json_data['name']}, {json_data['sys']['country']}",
        "timestamp": datetime.datetime.fromtimestamp(json_data["dt"]).strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "description": json_data["weather"][0]["description"],
        "temp": json_data["main"]["temp"],
        "temp_max": json_data["main"]["temp_max"],
        "temp_min": json_data["main"]["temp_min"],
        "humidity": json_data["main"]["humidity"],
        "wind_speed": json_data["wind"]["speed"],
        "cloud_coverage": json_data["clouds"]["all"],
    }


def get_darksky_weather(lat, lng):
    url = f"{DARKSKY_BASE_URL}/{DARKSKY_SECRET_KEY}/{lat},{lng}"
    return requests.get(url).json()


def get_openweather_forecast(city_id):
    url = f"{OPENWEATHER_BASE_URL}/forecast?id={city_id}&APPID={OPENWEATHER_APP_ID}&units=metric"
    return requests.get(url).json()


def get_openweather_weather(city_id):
    url = f"{OPENWEATHER_BASE_URL}/weather?id={city_id}&APPID={OPENWEATHER_APP_ID}&units=metric"
    return parse_openweather_weather(requests.get(url).json())


def get_stormglass_weather(lat, lng):
    url = f"{STORMGLASS_BASE_URL}?lat={lat}&lng={lng}"
    return requests.get(url, headers={"Authorization": STORMGLASS_API_KEY}).json()


if __name__ == "__main__":
    # print_weather(get_openweather_weather(OPENWEATHER_FLORIANOPOLIS_ID))
    # print(get_darksky_weather(-27.5, -48.5))
    # print(get_stormglass_weather(-27.5, -48.5))
    pass
