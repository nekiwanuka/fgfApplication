from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlantViewSet, MedicinalPlantViewSet, PlantNameViewSet, PlantImageGalleryViewSet, MedicinalPlantImageGalleryViewSet, PlantVideoGalleryViewSet

router = DefaultRouter()
router.register(r'plants', PlantViewSet)
router.register(r'medicinal-plants', MedicinalPlantViewSet)
router.register(r'plant-names', PlantNameViewSet)
router.register(r'plant-image-gallery', PlantImageGalleryViewSet)
router.register(r'medicinal-plant-image-gallery', MedicinalPlantImageGalleryViewSet)
router.register(r'plant-video-gallery', PlantVideoGalleryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]