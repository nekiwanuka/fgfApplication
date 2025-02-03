from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnimalProfileViewSet, AnimalClassificationViewSet, AnimalLocalNameViewSet, EntryCounterViewSet

router = DefaultRouter()
router.register(r'animalprofiles', AnimalProfileViewSet)
router.register(r'animalclassifications', AnimalClassificationViewSet)
router.register(r'animallocalnames', AnimalLocalNameViewSet)
router.register(r'entrycounters', EntryCounterViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
