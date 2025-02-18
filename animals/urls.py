from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnimalProfileViewSet, AnimalClassificationViewSet, AnimalLocalNameViewSet, AnimalImageGalleryViewSet, AnimalVideoGalleryViewSet, EntryCounterViewSet

router = DefaultRouter()
router.register(r'animal-profiles', AnimalProfileViewSet)
router.register(r'animal-classifications', AnimalClassificationViewSet)
router.register(r'animal-local-names', AnimalLocalNameViewSet)
router.register(r'animal-image-galleries', AnimalImageGalleryViewSet)
router.register(r'animal-video-galleries', AnimalVideoGalleryViewSet)
router.register(r'entrycounters', EntryCounterViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
