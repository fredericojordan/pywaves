from django.shortcuts import render
from core.models import Forecast


def homepage(request):
    forecast = (
        Forecast.objects.filter(spot__name__icontains="cruz")
        .order_by("-created")
        .first()
    )
    if not forecast:
        forecast = Forecast.objects.order_by("-created").first()
    return render(request, "chart.html", {"forecast": forecast})
