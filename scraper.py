import os
from datetime import datetime

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


def fahr_to_celsius(degrees_fahrenheit):
    return (degrees_fahrenheit - 32) * (5 / 9)


def direction_to_arrow(direction):
    if direction < 22.5 or direction > 317.5:
        return "↓"
    if direction < 67.5:
        return "↙"
    if direction < 112.5:
        return "←"
    if direction < 157.5:
        return "↖"
    if direction < 202.5:
        return "↑"
    if direction < 247.5:
        return "↗"
    if direction < 292.5:
        return "→"
    return "↘"


def print_weather(json_data):
    title = f"Weather conditions for {json_data.get('name')}:"
    print("-" * len(title))
    print(title)
    print("-" * len(title))

    if "timestamp" in json_data:
        print(f"Timestamp:      {json_data.get('timestamp')}")
    if "description" in json_data:
        print(f"Weather:        {json_data.get('description')}")
    if "temp" in json_data:
        print(f"Temperature:    {json_data.get('temp'):.1f} °C")
    if "temp_min" in json_data:
        print(
            f"Temp. range:    {json_data.get('temp_min'):.1f} - {json_data.get('temp_max'):.1f} °C"
        )
    if "humidity" in json_data:
        print(f"Humidity:       {json_data.get('humidity')} %")

    if "wave_height" in json_data:
        print(f"Wave height:    {json_data.get('wave_height'):.1f} m")
    if "wave_direction" in json_data:
        dir = json_data.get("wave_direction")
        print(f"Wave direction: {dir:.0f} {direction_to_arrow(dir)}")
    if "wave_period" in json_data:
        print(f"Wave period:    {json_data.get('wave_period'):.1f}")

    if "wind_speed" in json_data:
        print(f"Wind speed:     {json_data.get('wind_speed'):.1f} m/s")
    if "wind_gusts" in json_data:
        print(f"Wind gusts:     {json_data.get('wind_gusts'):.1f} m/s")
    if "wind_direction" in json_data:
        dir = json_data.get("wind_direction")
        print(f"Wind direction: {dir:.0f} {direction_to_arrow(dir)}")

    if "cloud_coverage" in json_data:
        print(f"Cloud cover:    {json_data.get('cloud_coverage'):.0f} %")
    print("-" * len(title))


def get_openweather_forecast(city_id):
    url = f"{OPENWEATHER_BASE_URL}/forecast?id={city_id}&APPID={OPENWEATHER_APP_ID}&units=metric"
    return requests.get(url).json()


def get_openweather_weather(city_id):
    url = f"{OPENWEATHER_BASE_URL}/weather?id={city_id}&APPID={OPENWEATHER_APP_ID}&units=metric"
    return parse_openweather_weather(requests.get(url).json())


def parse_openweather_weather(json_data):
    return {
        "name": f"{json_data['name']}, {json_data['sys']['country']}",
        "timestamp": datetime.datetime.fromtimestamp(json_data["dt"]).strftime(
            "%Y-%m-%d %H:%M"
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
    return parse_darksky_weather(requests.get(url).json())


def parse_darksky_weather(json_data):
    return {
        "name": f"{json_data['latitude']:.1f}, {json_data['longitude']:.1f}",
        "timestamp": datetime.fromtimestamp(json_data["currently"]["time"]).strftime(
            "%Y-%m-%d %H:%M"
        ),
        "description": json_data["currently"]["summary"],
        "temp": fahr_to_celsius(json_data["currently"]["temperature"]),
        "temp_max": fahr_to_celsius(json_data["daily"]["data"][0]["temperatureHigh"]),
        "temp_min": fahr_to_celsius(json_data["daily"]["data"][0]["temperatureLow"]),
        "humidity": json_data["currently"]["humidity"],
        "wind_speed": json_data["currently"]["windSpeed"],
        "wind_gusts": json_data["currently"]["windGust"],
        "cloud_coverage": 100 * json_data["currently"]["cloudCover"],
    }


def get_stormglass_weather(lat, lng):
    url = f"{STORMGLASS_BASE_URL}?lat={lat}&lng={lng}"
    headers = {"Authorization": STORMGLASS_API_KEY}
    return parse_stormglass_weather(requests.get(url, headers=headers).json())


def average_values(measurements):
    return sum([m["value"] for m in measurements]) / len(measurements)


def parse_stormglass_weather(json_data):
    """
    time: Timestamp in UTC
    airTemperature:  Air temperature in degrees celsius
    airPressure:  Air pressure in hPa
    cloudCover: Total cloud coverage in percent
    currentDirection: Direction of current. 0° indicates current coming from north
    currentSpeed: Speed of current in meters per second
    gust: Wind gust in meters per second
    humidity: Relative humidity in percent
    iceCover: Proportion, 0-1
    precipitation: Mean precipitation in kg/m²
    seaLevel: Height of sea level in MLLW in meters (tide)
    snowDepth: Depth of snow in meters
    swellDirection: Direction of swell waves. 0° indicates swell coming from north
    swellHeight: Height of swell waves in meters
    swellPeriod: Period of swell waves in seconds
    secondarySwellPeriod: Direction of secondary swell waves. 0° indicates swell coming from north
    secondarySwellDirection: Height of secondary swell waves in meters
    secondarySwellHeight: Period of secondary swell waves in seconds
    visiblity: Horizontal visibility in km
    waterTemperature: Water temperature in degrees celsius
    waveDirection: Direction of combined wind and swell waves. 0° indicates waves coming from north
    waveHeight: Height of combined wind and swell waves in meters
    wavePeriod: Period of combined wind and swell waves in seconds
    windWaveDirection: Direction of wind waves. 0° indicates waves coming from north
    windWaveHeight: Height of wind waves in meters
    windWavePeriod: Period of wind waves in seconds
    windDirection: Direction of wind. 0° indicates wind coming from north
    windSpeed: Speed of wind in meters per second
    """
    first_data_point = json_data["hours"][0]
    return {
        "name": f"{json_data['meta']['lat']:.1f}, {json_data['meta']['lng']:.1f}",
        "timestamp": datetime.fromisoformat(first_data_point["time"]).strftime(
            "%Y-%m-%d %H:%M"
        ),
        "temp": average_values(first_data_point["airTemperature"]),
        "humidity": average_values(first_data_point["humidity"]),
        "wind_speed": average_values(first_data_point["windSpeed"]),
        "wind_gusts": average_values(first_data_point["gust"]),
        "wind_direction": average_values(first_data_point["windDirection"]),
        "wave_height": average_values(first_data_point["waveHeight"]),
        "wave_period": average_values(first_data_point["wavePeriod"]),
        "wave_direction": average_values(first_data_point["waveDirection"]),
        "water_temperature": average_values(first_data_point["waterTemperature"]),
        "cloud_coverage": average_values(first_data_point["cloudCover"]),
    }


if __name__ == "__main__":
    # print_weather(get_openweather_weather(OPENWEATHER_FLORIANOPOLIS_ID))
    # print_weather(get_darksky_weather(-27.5, -48.5))
    print_weather(get_stormglass_weather(-27.5, -48.5))
