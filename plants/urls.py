from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PlantViewSet, PlantLocalNameViewSet, LanguageViewSet, MedicinalPlantViewSet,
    PlantImageGalleryViewSet, PlantVideoGalleryViewSet,
    scientificClassificationViewSet
)

router = DefaultRouter()
router.register(r'plants', PlantViewSet)
router.register(r'plant-local-names', PlantLocalNameViewSet)
router.register(r'languages', LanguageViewSet)
router.register(r'medicinal-plants', MedicinalPlantViewSet)
router.register(r'plant-images', PlantImageGalleryViewSet)
router.register(r'plant-videos', PlantVideoGalleryViewSet)
router.register(r'scientific-clarifications', scientificClassificationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
