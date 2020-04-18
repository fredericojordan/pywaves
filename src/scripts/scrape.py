from core.models import Spot


def run(*args):
    print("Scraping data...")
    for spot in Spot.objects.all():
        spot.save_forecast()
