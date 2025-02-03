from rest_framework import viewsets, permissions, filters
from drf_yasg.utils import swagger_auto_schema
from .models import Plant, MedicinalPlant, PlantLocalName, PlantImageGallery, MedicinalPlantImageGallery, PlantVideoGallery
from .serializers import PlantSerializer, MedicinalPlantSerializer, PlantNameSerializer, PlantImageGallerySerializer, MedicinalPlantImageGallerySerializer, PlantVideoGallerySerializer
from accounts.permissions import IsSuperUser, IsEditorOrSuperUser, IsContributorOrReadOnly

class PlantViewSet(viewsets.ModelViewSet):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer
    permission_classes = [IsContributorOrReadOnly]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['scientific_name', 'english_name', 'distribution_in_Uganda', 'unique_habitat']
    ordering_fields = ['scientific_name', 'english_name', 'date_added']

    @swagger_auto_schema(tags=['Plants'])
    def perform_create(self, serializer):
        # Automatically associate the plant with the logged-in user (contributor)
        serializer.save(contributor=self.request.user)

    @swagger_auto_schema(tags=['Plants'])
    def perform_update(self, serializer):
        # Contributors should not be able to update certain fields like 'status'
        if not self.request.user.is_staff:  # Check if the user is not a staff member
            # Ensure restricted fields (like 'status') cannot be modified
            serializer.validated_data.pop('status', None)
        super().perform_update(serializer)

class MedicinalPlantViewSet(viewsets.ModelViewSet):
    queryset = MedicinalPlant.objects.all()
    serializer_class = MedicinalPlantSerializer
    permission_classes = [IsContributorOrReadOnly]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['plant__scientific_name', 'plant__english_name', 'health_issues']
    ordering_fields = ['plant__scientific_name', 'plant__english_name']

    @swagger_auto_schema(tags=['Medicinal Plants'])
    def perform_create(self, serializer):
        serializer.save(contributor=self.request.user)

class PlantNameViewSet(viewsets.ModelViewSet):
    queryset = PlantLocalName.objects.all()
    serializer_class = PlantNameSerializer
    permission_classes = [IsContributorOrReadOnly]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['local_name', 'language', 'plant__scientific_name', 'plant__english_name']
    ordering_fields = ['local_name', 'language']

    @swagger_auto_schema(tags=['Plant Names'])
    def perform_create(self, serializer):
        serializer.save(contributor=self.request.user)

class PlantImageGalleryViewSet(viewsets.ModelViewSet):
    queryset = PlantImageGallery.objects.all()
    serializer_class = PlantImageGallerySerializer
    permission_classes = [IsEditorOrSuperUser]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['plant__scientific_name', 'plant__english_name', 'caption']
    ordering_fields = ['plant__scientific_name', 'plant__english_name']

    @swagger_auto_schema(tags=['Plant Image Gallery'])
    def perform_create(self, serializer):
        serializer.save(contributor=self.request.user)

class MedicinalPlantImageGalleryViewSet(viewsets.ModelViewSet):
    queryset = MedicinalPlantImageGallery.objects.all()
    serializer_class = MedicinalPlantImageGallerySerializer
    permission_classes = [IsEditorOrSuperUser]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['medicinal_plant__plant__scientific_name', 'medicinal_plant__plant__english_name', 'caption']
    ordering_fields = ['medicinal_plant__plant__scientific_name', 'medicinal_plant__plant__english_name']

    @swagger_auto_schema(tags=['Medicinal Plant Image Gallery'])
    def perform_create(self, serializer):
        serializer.save(contributor=self.request.user)

class PlantVideoGalleryViewSet(viewsets.ModelViewSet):
    queryset = PlantVideoGallery.objects.all()
    serializer_class = PlantVideoGallerySerializer
    permission_classes = [IsEditorOrSuperUser]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['plant__scientific_name', 'plant__english_name', 'caption']
    ordering_fields = ['plant__scientific_name', 'plant__english_name']

    @swagger_auto_schema(tags=['Plant Video Gallery'])
    def perform_create(self, serializer):
        serializer.save(contributor=self.request.user)