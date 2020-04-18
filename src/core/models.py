from django.contrib.gis.db import models as gis_models
from django.db import models
from django.utils.translation import ugettext as _
from django_extensions.db.fields.json import JSONField
from django_extensions.db.models import TimeStampedModel

from utils.stormglass import get_stormglass_weather, print_weather, average_sources


class Forecast(TimeStampedModel):
    spot = models.ForeignKey(
        "core.Spot", on_delete=models.PROTECT, related_name="forecasts"
    )
    raw_data = JSONField(
        null=False, blank=False, help_text=_("Raw json data from API response")
    )

    def __str__(self):
        return f"{self.spot} @ {self.created.strftime('%Y-%m-%d %H:%M')}"

    @property
    def ordered_data_points(self):
        return self.data_points.order_by("timestamp")

    @property
    def report(self):
        return (
            self.data_points.order_by("timestamp")
            .filter(timestamp__gte=self.created)
            .first()
        )


class DataPoint(TimeStampedModel):
    forecast = models.ForeignKey(
        "core.Forecast", on_delete=models.CASCADE, related_name="data_points"
    )

    timestamp = models.DateTimeField(null=True, blank=True)

    temperature = models.DecimalField(
        null=True, blank=True, decimal_places=2, max_digits=6
    )
    humidity = models.IntegerField(null=True, blank=True)
    cloud_cover = models.IntegerField(null=True, blank=True)

    wave_height = models.DecimalField(
        null=True, blank=True, decimal_places=2, max_digits=6
    )
    wave_direction = models.IntegerField(null=True, blank=True)
    wave_period = models.DecimalField(
        null=True, blank=True, decimal_places=2, max_digits=6
    )

    wind_speed = models.DecimalField(
        null=True, blank=True, decimal_places=2, max_digits=6
    )
    wind_gusts = models.DecimalField(
        null=True, blank=True, decimal_places=2, max_digits=6
    )
    wind_direction = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.forecast.spot} @ {self.timestamp.strftime('%Y-%m-%d %H:%M')}"


class Spot(TimeStampedModel):
    name = models.CharField(max_length=100, help_text=_("Surfing spot name"))
    location = gis_models.PointField(blank=False, null=False)

    def __str__(self):
        coords = f"{self.latitude:.1f}, {self.longitude:.1f}"

        if self.name:
            return f"{self.name} ({coords})"
        return f"({coords})"

    @property
    def longitude(self):
        return self.location.coords[0]

    @property
    def latitude(self):
        return self.location.coords[1]

    def fetch_forecast(self):
        return get_stormglass_weather(self.latitude, self.longitude)

    def print_forecast(self):
        print_weather(self.fetch_forecast())

    def save_forecast(self):
        json_data = self.fetch_forecast()
        forecast = Forecast.objects.create(spot=self, raw_data=json_data)
        DataPoint.objects.bulk_create(
            [
                DataPoint(
                    forecast=forecast,
                    timestamp=entry.get("time"),
                    temperature=average_sources(entry.get("airTemperature")),
                    humidity=average_sources(entry.get("humidity")),
                    cloud_cover=average_sources(entry.get("cloudCover")),
                    wave_height=average_sources(entry.get("waveHeight")),
                    wave_direction=average_sources(entry.get("waveDirection")),
                    wave_period=average_sources(entry.get("wavePeriod")),
                    wind_speed=average_sources(entry.get("windSpeed")),
                    wind_gusts=average_sources(entry.get("gust")),
                    wind_direction=average_sources(entry.get("windDirection")),
                )
                for entry in json_data.get("hours", [])
            ]
        )
        return json_data
