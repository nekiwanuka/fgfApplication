from django.urls import path, include
from django.contrib import admin
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

# API schema view
schema_view = get_schema_view(
    openapi.Info(
        title="Your Project API",
        default_version='v1',
        description="Detailed API description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@yourproject.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Project URLs
urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),  # Ensure the namespace is unique
    path('accounts/', include('accounts.urls')),
    path('animals/', include('animals.urls')),
    path("i18n/", include("django.conf.urls.i18n")),
    path('plants/', include('plants.urls')),
    path('cultures/', include('cultures.urls')),
    path('grappelli/', include('grappelli.urls')),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    #path("i18n/", include("django.conf.urls.i18n")),
]




# Serve media and static files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)