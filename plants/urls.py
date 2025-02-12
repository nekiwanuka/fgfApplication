from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PlantViewSet, PlantLocalNameViewSet, LanguageViewSet, MedicinalPlantViewSet,
    PlantImageGalleryViewSet, PlantVideoGalleryViewSet,
PlantScientificClassificationViewSet
)

router = DefaultRouter()
router.register(r'plant-profile', PlantViewSet)
router.register(r'plant-local-names', PlantLocalNameViewSet)
router.register(r'languages', LanguageViewSet)
router.register(r'medicinal-plants', MedicinalPlantViewSet)
router.register(r'plant-images', PlantImageGalleryViewSet)
router.register(r'plant-videos', PlantVideoGalleryViewSet)
router.register(r'plant-scientific-clarifications', PlantScientificClassificationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
