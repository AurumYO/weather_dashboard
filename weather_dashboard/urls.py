from django.conf import settings
from django.contrib import admin
from django.urls import include
from django.urls import path
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Weather Dashboard API",
        default_version="v1",
        description="API documentation for the Weather Dashboard project",
        contact=openapi.Contact(email=settings.CONTACT_EMAIL),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("weather.urls")),
    # Swagger UI:
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("dashboard/", include("dashboard.urls")),
]
