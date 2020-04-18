import requests
from django.conf import settings

STORMGLASS_BASE_URL = "https://api.stormglass.io/v1/weather/point"


def fahr_to_celsius(degrees_fahrenheit):
    return (degrees_fahrenheit - 32) * (5 / 9)


def direction_to_arrow(direction):
    if direction < 22.5 or direction > 337.5:
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
    if "temp" in json_data:
        print(f"Temperature:    {json_data.get('temp'):.1f} °C")
    if "temp_min" in json_data and "temp_max" in json_data:
        print(
            f"Temp. range:    {json_data.get('temp_min'):.1f} - {json_data.get('temp_max'):.1f} °C"
        )

    if "wave_height" in json_data:
        print(f"Wave height:    {json_data.get('wave_height'):.1f} m")
    if "wave_direction" in json_data:
        dir = json_data.get("wave_direction")
        print(f"Wave direction: {dir:.0f} {direction_to_arrow(dir)}")
    if "wave_period" in json_data:
        print(f"Wave period:    {json_data.get('wave_period'):.1f} s")

    if "wind_speed" in json_data:
        print(f"Wind speed:     {json_data.get('wind_speed'):.1f} m/s")
    if "wind_gusts" in json_data:
        print(f"Wind gusts:     {json_data.get('wind_gusts'):.1f} m/s")
    if "wind_direction" in json_data:
        dir = json_data.get("wind_direction")
        print(f"Wind direction: {dir:.0f} {direction_to_arrow(dir)}")

    if "description" in json_data:
        print(f"Weather:        {json_data.get('description')}")
    if "humidity" in json_data:
        print(f"Humidity:       {json_data.get('humidity'):.0f} %")
    if "cloud_coverage" in json_data:
        print(f"Cloud cover:    {json_data.get('cloud_coverage'):.0f} %")
    print("-" * len(title))


def get_stormglass_weather(lat, lng):
    url = f"{STORMGLASS_BASE_URL}?lat={lat}&lng={lng}"
    headers = {"Authorization": settings.STORMGLASS_API_KEY}
    return requests.get(url, headers=headers).json()


def average_sources(measurements):
    if not measurements or len(measurements) == 0:
        return None
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
        "timestamp": first_data_point["time"],
        "temperatures": average_sources(first_data_point["airTemperature"]),
        "humidity": average_sources(first_data_point["humidity"]),
        "wind_speed": average_sources(first_data_point["windSpeed"]),
        "wind_gusts": average_sources(first_data_point["gust"]),
        "wind_direction": average_sources(first_data_point["windDirection"]),
        "wave_height": average_sources(first_data_point["waveHeight"]),
        "wave_period": average_sources(first_data_point["wavePeriod"]),
        "wave_direction": average_sources(first_data_point["waveDirection"]),
        "water_temperature": average_sources(first_data_point["waterTemperature"]),
        "cloud_coverage": average_sources(first_data_point["cloudCover"]),
        "_raw_data": json_data,
    }
