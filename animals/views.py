from rest_framework import viewsets
from .models import AnimalProfile, AnimalClassification, AnimalLocalName, EntryCounter
from .serializers import AnimalProfileSerializer, AnimalClassificationSerializer, AnimalLocalNameSerializer, EntryCounterSerializer

class AnimalProfileViewSet(viewsets.ModelViewSet):
    queryset = AnimalProfile.objects.all()
    serializer_class = AnimalProfileSerializer


class AnimalClassificationViewSet(viewsets.ModelViewSet):
    queryset = AnimalClassification.objects.all()
    serializer_class = AnimalClassificationSerializer


class AnimalLocalNameViewSet(viewsets.ModelViewSet):
    queryset = AnimalLocalName.objects.all()
    serializer_class = AnimalLocalNameSerializer


class EntryCounterViewSet(viewsets.ModelViewSet):
    queryset = EntryCounter.objects.all()
    serializer_class = EntryCounterSerializer
