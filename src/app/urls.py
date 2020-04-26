from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

admin.site.site_header = "PyWaves Administration"
admin.site.site_title = "PyWaves Admin Portal"
admin.site.index_title = "Welcome to PyWaves Administration Portal"

schema_view = get_schema_view(
    openapi.Info(
        title="PyWaves API",
        default_version="v1",
        description="Documentation for PyWaves API endpoints.",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("docs/", schema_view.with_ui("swagger", cache_timeout=0), name="docs"),
    path("", include("core.urls")),
    path("", include("messaging.urls")),
]
