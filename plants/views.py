from rest_framework import viewsets, permissions
from .models import Plant, MedicinalPlant, PlantLocalName, PlantImageGallery, MedicinalPlantImageGallery, PlantVideoGallery
from .serializers import PlantSerializer, MedicinalPlantSerializer, PlantNameSerializer, PlantImageGallerySerializer, MedicinalPlantImageGallerySerializer, PlantVideoGallerySerializer
from accounts.permissions import IsSuperUser, IsEditorOrSuperUser, IsContributorOrReadOnly

class PlantViewSet(viewsets.ModelViewSet):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer
    permission_classes = [IsContributorOrReadOnly]  # Ensures contributors can only read or create
        
    def perform_create(self, serializer):
        # Automatically associate the plant with the logged-in user (contributor)
        serializer.save(contributor=self.request.user)

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

    def perform_create(self, serializer):
        serializer.save(contributor=self.request.user)

class PlantNameViewSet(viewsets.ModelViewSet):
    queryset = PlantLocalName.objects.all()
    serializer_class = PlantNameSerializer
    permission_classes = [IsContributorOrReadOnly]

class PlantImageGalleryViewSet(viewsets.ModelViewSet):
    queryset = PlantImageGallery.objects.all()
    serializer_class = PlantImageGallerySerializer
    permission_classes = [IsEditorOrSuperUser]

class MedicinalPlantImageGalleryViewSet(viewsets.ModelViewSet):
    queryset = MedicinalPlantImageGallery.objects.all()
    serializer_class = MedicinalPlantImageGallerySerializer
    permission_classes = [IsEditorOrSuperUser]

class PlantVideoGalleryViewSet(viewsets.ModelViewSet):
    queryset = PlantVideoGallery.objects.all()
    serializer_class = PlantVideoGallerySerializer
    permission_classes = [IsEditorOrSuperUser]