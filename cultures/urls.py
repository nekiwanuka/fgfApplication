from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EthnicGroupViewSet, EthnicityViewSet, CulturalKingdomViewSet, ClanViewSet, ClanProfileViewSet

router = DefaultRouter()
router.register(r'ethnic-groups', EthnicGroupViewSet)
router.register(r'ethnicities', EthnicityViewSet)
router.register(r'cultural-kingdoms', CulturalKingdomViewSet)
router.register(r'clans', ClanViewSet)
router.register(r'clan-profiles', ClanProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
