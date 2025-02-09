from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from accounts.permissions import IsContributorOrReadOnly, IsEditorOrSuperUser
from .models import (
    Plant, PlantLocalName, Language, MedicinalPlant, PlantImageGallery,
    PlantVideoGallery, scientificClassification
)
from .serializers import (
    PlantSerializer, PlantLocalNameSerializer, LanguageSerializer,
    MedicinalPlantSerializer, PlantImageGallerySerializer,
    PlantVideoGallerySerializer, scientificClassificationSerializer
)


class PlantViewSet(viewsets.ModelViewSet):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer
    permission_classes = [IsContributorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['english_name', 'scientific_name', 'life_form', 'status', 'contributor']

    def perform_create(self, serializer):
        serializer.save(contributor=self.request.user)

class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = [IsContributorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['name']
    ordering_fields = ['name']

class PlantLocalNameViewSet(viewsets.ModelViewSet):
    queryset = PlantLocalName.objects.all()
    serializer_class = PlantLocalNameSerializer
    permission_classes = [IsContributorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['plant', 'language', 'local_name']
    search_fields = ['local_name']
    ordering_fields = ['local_name']

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        plant = serializer.validated_data['plant']
        language = serializer.validated_data['language']
        local_name = serializer.validated_data['local_name']

        if PlantLocalName.objects.filter(plant=plant, language=language, local_name=local_name).exists():
            return Response({'error': 'This local name already exists for this plant in the given language.'},
                            status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MedicinalPlantViewSet(viewsets.ModelViewSet):
    queryset = MedicinalPlant.objects.all()
    serializer_class = MedicinalPlantSerializer
    permission_classes = [IsContributorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['plant', 'health_issues', 'part_used', 'shelf_life', 'contributor']
    search_fields = ['health_issues', 'cultural_value', 'contraindications', 'preparation_steps']
    ordering_fields = ['shelf_life', 'created_at']

class PlantImageGalleryViewSet(viewsets.ModelViewSet):
    queryset = PlantImageGallery.objects.all()
    serializer_class = PlantImageGallerySerializer
    permission_classes = [IsContributorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['plant']
    search_fields = ['description']
    ordering_fields = ['created_at']

class PlantVideoGalleryViewSet(viewsets.ModelViewSet):
    queryset = PlantVideoGallery.objects.all()
    serializer_class = PlantVideoGallerySerializer
    permission_classes = [IsEditorOrSuperUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['plant']
    search_fields = ['description']
    ordering_fields = ['created_at']


class scientificClassificationViewSet(viewsets.ModelViewSet):
    queryset = scientificClassification.objects.all()
    serializer_class = scientificClassificationSerializer
    permission_classes = [IsContributorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['kingdom', 'order', 'family', 'genus', 'species']
    search_fields = ['kingdom', 'order', 'family', 'genus', 'species']
    ordering_fields = ['kingdom', 'order', 'family', 'genus', 'species']
