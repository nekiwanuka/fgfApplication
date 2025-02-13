from rest_framework import viewsets, permissions
from .models import EthnicGroup, Ethnicity, CulturalKingdom, Clan
from .serializers import (
    EthnicGroupSerializer, EthnicitySerializer, CulturalKingdomSerializer, ClanSerializer, ClanProfileSerializer
)
from accounts.permissions import IsSuperUser, IsContributorOrReadOnly, IsEditorOrSuperUser

class EthnicGroupViewSet(viewsets.ModelViewSet):
    """Handles CRUD operations for EthnicGroup."""
    queryset = EthnicGroup.objects.all()
    serializer_class = EthnicGroupSerializer
    permission_classes = [IsEditorOrSuperUser | IsContributorOrReadOnly]

class EthnicityViewSet(viewsets.ModelViewSet):
    """Handles CRUD operations for Ethnicity."""
    queryset = Ethnicity.objects.all()
    serializer_class = EthnicitySerializer
    permission_classes = [IsEditorOrSuperUser | IsContributorOrReadOnly]

class CulturalKingdomViewSet(viewsets.ModelViewSet):
    """Handles CRUD operations for CulturalKingdom."""
    queryset = CulturalKingdom.objects.all()
    serializer_class = CulturalKingdomSerializer
    permission_classes = [IsEditorOrSuperUser| IsContributorOrReadOnly]

class ClanViewSet(viewsets.ModelViewSet):
    """Handles CRUD operations for Clan."""
    queryset = Clan.objects.all()
    serializer_class = ClanSerializer
    permission_classes = [IsEditorOrSuperUser | IsContributorOrReadOnly]

class ClanProfileViewSet(viewsets.ModelViewSet):
    """Handles CRUD operations for ClanProfile."""
    queryset = Clan.objects.all()
    serializer_class = ClanProfileSerializer
    permission_classes = [IsEditorOrSuperUser]