from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlantViewSet, MedicinalPlantViewSet, PlantNameViewSet, PlantImageGalleryViewSet, MedicinalPlantImageGalleryViewSet, PlantVideoGalleryViewSet

router = DefaultRouter()
router.register(r'plants', PlantViewSet, basename='plant')
router.register(r'medicinal-plants', MedicinalPlantViewSet, basename='medicinal-plant')
router.register(r'plant-names', PlantNameViewSet, basename='plant-name')
router.register(r'plant-image-gallery', PlantImageGalleryViewSet, basename='plant-image-gallery')
router.register(r'medicinal-plant-image-gallery', MedicinalPlantImageGalleryViewSet, basename='medicinal-plant-image-gallery')
router.register(r'plant-video-gallery', PlantVideoGalleryViewSet, basename='plant-video-gallery')

urlpatterns = [
    path('', include(router.urls)),
]
