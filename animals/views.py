from requests import Response, request
from rest_framework import status
from rest_framework import viewsets, filters
from .models import AnimalProfile, AnimalClassification, AnimalLocalName, EntryCounter
from .serializers import AnimalProfileSerializer, AnimalClassificationSerializer, AnimalLocalNameSerializer, EntryCounterSerializer
from accounts.permissions import IsContributorOrReadOnly, IsEditorOrSuperUser


class AnimalProfileViewSet(viewsets.ModelViewSet):
    queryset = AnimalProfile.objects.all()  # No soft delete filter
    serializer_class = AnimalProfileSerializer
    permission_classes = [IsContributorOrReadOnly]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['english_name', 'scientific_name', 'description', 'areas_in_Uganda']
    ordering_fields = ['english_name', 'scientific_name', 'date_entered']

    def perform_create(self, serializer):
        """Set default values and contributor during creation."""
        user = self.request.user
        serializer.save(contributor=[user], status='draft')  # Ensure 'status' is set to 'draft'

    def perform_update(self, serializer):
        """Prevent contributors from modifying protected fields."""
        user = self.request.user
        instance = self.get_object()

        # Fields that contributors CANNOT modify
        protected_fields = ['status', 'review_feedback', 'citation', 'created_at', 'updated_at']

        # If the user is a contributor, remove protected fields from update
        if not user.is_staff:
            for field in protected_fields:
                serializer.validated_data.pop(field, None)

        serializer.save()


class AnimalClassificationViewSet(viewsets.ModelViewSet):
    queryset = AnimalClassification.objects.all()  # Removed soft delete filter
    serializer_class = AnimalClassificationSerializer
    permission_classes = [IsContributorOrReadOnly]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['kingdom_name', 'species', 'animal_class', 'order']
    ordering_fields = ['kingdom_name', 'species', 'animal_class']


class AnimalLocalNameViewSet(viewsets.ModelViewSet):
    queryset = AnimalLocalName.objects.all()  # Removed soft delete filter
    serializer_class = AnimalLocalNameSerializer
    permission_classes = [IsContributorOrReadOnly]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['local_name', 'language', 'animal__english_name', 'animal__scientific_name']
    ordering_fields = ['local_name', 'language']

class EntryCounterViewSet(viewsets.ModelViewSet):
    queryset = EntryCounter.objects.all()
    serializer_class = EntryCounterSerializer
    permission_classes = [IsEditorOrSuperUser]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['total_entries']
