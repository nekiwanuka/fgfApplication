from rest_framework import viewsets, permissions, filters
from rest_framework.response import Response
from .models import AnimalClassification, AnimalProfile, AnimalLocalName, AnimalEntryCounter
from .serializers import (
    AnimalClassificationSerializer,
    AnimalProfileSerializer,
    AnimalLocalNameSerializer,
    AnimalLocalNameCreateSerializer,
    AnimalEntryCounterSerializer,
)
from accounts.permissions import IsContributorOrReadOnly

class AnimalClassificationViewSet(viewsets.ModelViewSet):
    queryset = AnimalClassification.objects.all()
    serializer_class = AnimalClassificationSerializer
    permission_classes = [permissions.IsAuthenticated, IsContributorOrReadOnly]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['kingdom_name', 'species', 'animal_class', 'order']
    ordering_fields = ['kingdom_name', 'created_at']


class AnimalProfileViewSet(viewsets.ModelViewSet):
    queryset = AnimalProfile.objects.all()
    serializer_class = AnimalProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsContributorOrReadOnly]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['english_name', 'scientific_name', 'description', 'areas_in_Uganda']
    ordering_fields = ['english_name', 'date_entered']

    def perform_create(self, serializer):
        # Save the AnimalProfile instance
        animal_profile = serializer.save()

        # Increment the entry counter for animal profiles
        counter, created = AnimalEntryCounter.objects.get_or_create(id=1)
        counter.increment()

        return animal_profile


class AnimalLocalNameViewSet(viewsets.ModelViewSet):
    queryset = AnimalLocalName.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsContributorOrReadOnly]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['local_name', 'language', 'animal__english_name']
    ordering_fields = ['local_name', 'created_at']

    def get_serializer_class(self):
        # Use a different serializer for create/update
        if self.action in ['create', 'update']:
            return AnimalLocalNameCreateSerializer
        return AnimalLocalNameSerializer

    def perform_create(self, serializer):
        # Ensure the local name is added and contributor is saved automatically
        animal_local_name = serializer.save(contributor=self.request.user)

        # Increment the entry counter for the related animal
        counter, created = AnimalEntryCounter.objects.get_or_create(id=1)
        counter.increment()

        return animal_local_name


class AnimalEntryCounterViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AnimalEntryCounter.objects.all()
    serializer_class = AnimalEntryCounterSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['total_entries']
