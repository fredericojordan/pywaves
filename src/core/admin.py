from django import forms
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.gis.admin import OSMGeoAdmin

from core.models import Spot, Forecast


class SpotAdmin(OSMGeoAdmin):
    # map_template = "opencyclemap.html"
    pass


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
