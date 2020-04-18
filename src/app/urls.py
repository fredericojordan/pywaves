from django.contrib import admin
from django.urls import path


admin.site.site_header = "PyWaves Administration"
admin.site.site_title = "PyWaves Admin Portal"
admin.site.index_title = "Welcome to PyWaves Administration Portal"


urlpatterns = [
    path("", admin.site.urls),
]
