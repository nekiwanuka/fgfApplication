from rest_framework import viewsets, filters
from rest_framework.exceptions import PermissionDenied, ValidationError
from .models import AnimalProfile, AnimalClassification, AnimalLocalName, EntryCounter
from .serializers import (
    AnimalProfileSerializer, 
    AnimalClassificationSerializer, 
    AnimalClassificationNestedSerializer,  # Added for nested use
    AnimalLocalNameSerializer, 
    EntryCounterSerializer
)
from accounts.permissions import IsContributorOrReadOnly, IsEditorOrSuperUser

# ✅ Animal Profile ViewSet
class AnimalProfileViewSet(viewsets.ModelViewSet):
    queryset = AnimalProfile.objects.all()
    serializer_class = AnimalProfileSerializer
    permission_classes = [IsContributorOrReadOnly]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['english_name', 'scientific_name', 'description', 'areas_in_Uganda']
    ordering_fields = ['english_name', 'scientific_name', 'date_entered']

    def perform_create(self, serializer):
        """Set default values and add the current user as the contributor during creation."""
        user = self.request.user
        serializer.save(contributor=user, status='draft')

    def perform_update(self, serializer):
        """Allow contributors to edit only their own draft entries, restricting certain fields."""
        user = self.request.user
        instance = self.get_object()

        protected_fields = ['citation', 'created_at', 'updated_at']

        if user.is_staff:
            serializer.save()
            return

        if instance.status != 'draft' or instance.contributor != user:
            raise PermissionDenied("You can only edit your own draft entries.")

        for field in protected_fields:
            if field in serializer.validated_data:
                raise ValidationError({field: "You are not allowed to modify this field."})

        serializer.save()


# ✅ Animal Classification ViewSet (Handles Both Full and Nested Serializers)
class AnimalClassificationViewSet(viewsets.ModelViewSet):
    queryset = AnimalClassification.objects.all()
    permission_classes = [IsContributorOrReadOnly]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['kingdom_name', 'species', 'animal_class', 'order']
    ordering_fields = ['kingdom_name', 'species', 'animal_class']

    def get_serializer_class(self):
        """Return the appropriate serializer depending on the request context."""
        if self.action in ['list', 'retrieve']:  
            return AnimalClassificationSerializer  # Full data when accessed directly
        return AnimalClassificationNestedSerializer  # Use nested serializer when embedded


# ✅ Animal Local Name ViewSet
class AnimalLocalNameViewSet(viewsets.ModelViewSet):
    queryset = AnimalLocalName.objects.all()
    serializer_class = AnimalLocalNameSerializer
    permission_classes = [IsContributorOrReadOnly]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['local_name', 'language', 'animal__english_name', 'animal__scientific_name']
    ordering_fields = ['local_name', 'language']


# ✅ Entry Counter ViewSet
class EntryCounterViewSet(viewsets.ModelViewSet):
    queryset = EntryCounter.objects.all()
    serializer_class = EntryCounterSerializer
    permission_classes = [IsEditorOrSuperUser]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['total_entries']
