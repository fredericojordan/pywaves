from django.urls import include, path

from messaging.api.v1 import urls

app_name = "messaging"
urlpatterns = [path("api/v1/", include(urls))]
