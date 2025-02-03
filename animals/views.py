from rest_framework import viewsets, filters
from .models import AnimalProfile, AnimalClassification, AnimalLocalName, EntryCounter
from .serializers import AnimalProfileSerializer, AnimalClassificationSerializer, AnimalLocalNameSerializer, EntryCounterSerializer
from accounts.permissions import IsContributorOrReadOnly, IsContributor, IsEditorOrSuperUser

class AnimalProfileViewSet(viewsets.ModelViewSet):
    queryset = AnimalProfile.objects.all()
    serializer_class = AnimalProfileSerializer
    permission_classes = [IsContributorOrReadOnly]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['english_name', 'scientific_name', 'description', 'areas_in_Uganda']
    ordering_fields = ['english_name', 'scientific_name', 'date_entered']

    def perform_create(self, serializer):
        # Ensure 'status' is automatically set to 'draft' when creating a new AnimalProfile instance
        serializer.save(status='draft')

class AnimalClassificationViewSet(viewsets.ModelViewSet):
    queryset = AnimalClassification.objects.all()
    serializer_class = AnimalClassificationSerializer
    permission_classes = [IsContributor]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['kingdom_name', 'species', 'animal_class', 'order']
    ordering_fields = ['kingdom_name', 'species', 'animal_class']

class AnimalLocalNameViewSet(viewsets.ModelViewSet):
    queryset = AnimalLocalName.objects.all()
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