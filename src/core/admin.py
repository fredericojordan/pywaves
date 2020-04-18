from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.gis.admin import OSMGeoAdmin

from core.models import Spot, Forecast


class SpotAdmin(OSMGeoAdmin):
    # map_template = "opencyclemap.html"
    actions = ["get_forecast"]
    list_display = ["name", "latitude", "longitude"]

    def get_forecast(self, request, queryset):
        forecasts = []
        for spot in queryset:
            forecasts.append(spot.save_forecast())

        if len(forecasts) == 1:
            self.message_user(
                request,
                f"'{forecasts[0].spot}' forecast #{forecasts[0].pk} has been generated!",
            )
        if len(forecasts) > 1:
            self.message_user(
                request, f"{len(forecasts)} forecasts have been generated!"
            )

    get_forecast.short_description = "Fetch spot forecast via API and save results"


class ForecastAdmin(ModelAdmin):
    readonly_fields = ("spot", "created", "raw_data")
    fieldsets = (
        (None, {"fields": ("spot", "created")}),
        ("Raw Data", {"classes": ("collapse",), "fields": ("raw_data",)},),
    )
    list_filter = (
        "spot",
        "created",
    )
    list_display = (
        "id",
        "spot",
        "created",
    )

    change_form_template = "change_forecast.html"


admin.site.register(Spot, SpotAdmin)
admin.site.register(Forecast, ForecastAdmin)
