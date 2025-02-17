from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import EthnicGroup, Ethnicity, CulturalKingdom, Clan, ClanProfile
from .serializers import (
    EthnicGroupSerializer, EthnicitySerializer, CulturalKingdomSerializer, ClanSerializer, ClanProfileSerializer
)
from accounts.permissions import  IsContributorOrReadOnly, ReadOnlyOrEditorSuperUser

class EthnicGroupViewSet(viewsets.ModelViewSet):
    """Handles CRUD operations for EthnicGroup."""
    queryset = EthnicGroup.objects.all()
    serializer_class = EthnicGroupSerializer
    permission_classes = [IsContributorOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']  # Update field names as needed
    ordering_fields = ['name', 'created_at']  # Ensure these fields exist in your model

class EthnicityViewSet(viewsets.ModelViewSet):
    """Handles CRUD operations for Ethnicity."""
    queryset = Ethnicity.objects.all()
    serializer_class = EthnicitySerializer
    permission_classes = [IsContributorOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']

class CulturalKingdomViewSet(viewsets.ModelViewSet):
    """Handles CRUD operations for CulturalKingdom."""
    queryset = CulturalKingdom.objects.all()
    serializer_class = CulturalKingdomSerializer
    permission_classes = [IsContributorOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']

class ClanViewSet(viewsets.ModelViewSet):
    """Handles CRUD operations for Clan."""
    queryset = Clan.objects.all()
    serializer_class = ClanSerializer
    permission_classes = [IsContributorOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['clan_name', 'totem', 'clan_leader_name']
    ordering_fields = ['clan_name', 'date_entered']
    ordering = ['clan_name'] 
    
class ClanProfileViewSet(viewsets.ModelViewSet):
    """Handles CRUD operations for ClanProfile."""
    queryset = ClanProfile.objects.all().order_by('id')  # Ensure ordering
    serializer_class = ClanProfileSerializer
    permission_classes = [ReadOnlyOrEditorSuperUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['clan_name']
    ordering_fields = ['clan_name', 'date_entered']
