from rest_framework import viewsets
from yaml import serialize
from .models import AnimalProfile, AnimalClassification, AnimalLocalName, EntryCounter
from .serializers import AnimalProfileSerializer, AnimalClassificationSerializer, AnimalLocalNameSerializer, EntryCounterSerializer

class AnimalProfileViewSet(viewsets.ModelViewSet):
    queryset = AnimalProfile.objects.all()
    serializer_class = AnimalProfileSerializer
    def perform_create(self, serializer):
        # Ensure 'status' is automatically set to 'draft' when creating a new AnimalProfile instance
        serializer.save(status='draft')


class AnimalClassificationViewSet(viewsets.ModelViewSet):
    queryset = AnimalClassification.objects.all()
    serializer_class = AnimalClassificationSerializer


class AnimalLocalNameViewSet(viewsets.ModelViewSet):
    queryset = AnimalLocalName.objects.all()
    serializer_class = AnimalLocalNameSerializer


class EntryCounterViewSet(viewsets.ModelViewSet):
    queryset = EntryCounter.objects.all()
    serializer_class = EntryCounterSerializer
