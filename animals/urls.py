from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AnimalClassificationViewSet,
    AnimalProfileViewSet,
    AnimalLocalNameViewSet,
    AnimalEntryCounterViewSet
)

# Create a router and register all viewsets
router = DefaultRouter()
router.register(r'animal-classifications', AnimalClassificationViewSet, basename='animal-classification')
router.register(r'animal-profiles', AnimalProfileViewSet, basename='animal-profile')
router.register(r'animal-local-names', AnimalLocalNameViewSet, basename='animal-local-name')
router.register(r'animal-entry-counters', AnimalEntryCounterViewSet, basename='animal-entry-counter')  # New route

urlpatterns = [
    path('', include(router.urls)),
]
