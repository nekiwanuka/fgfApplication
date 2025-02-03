from rest_framework import serializers
from .models import Plant, Language, PlantLocalName, MedicinalPlant, MedicinalPlantName, ScientificClarification, PlantImageGallery, MedicinalPlantImageGallery, PlantVideoGallery
from accounts.models import FgfUser

class PlantNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantLocalName
        fields = ['plant_name_id', 'plant', 'language', 'LocalName']

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['language_id', 'name']

class PlantSerializer(serializers.ModelSerializer):
    plant_names = PlantNameSerializer(many=True, read_only=True)
    contributor = serializers.PrimaryKeyRelatedField(queryset=FgfUser.objects.all(), default=lambda: FgfUser.objects.first())
    language = serializers.PrimaryKeyRelatedField(queryset=Language.objects.all(), default=lambda: Language.objects.first())  # Ensure default is a Language object

    class Meta:
        model = Plant
        fields = '__all__'

    def to_representation(self, instance):
        # Get the original serialized data
        representation = super().to_representation(instance)
        
        # Get the request context (used to check user role)
        request = self.context.get('request')

        # If the user is a contributor, exclude the 'status' field from the response
        if request and request.user and not request.user.is_staff:  # Contributor check
            representation.pop('status', None)  # Exclude the status field from the response

        return representation

    def create(self, validated_data):
        # Automatically set the 'status' field to 'draft' when creating a new plant
        validated_data['status'] = 'draft'  # Set default status for new entries
        plant_name_data = validated_data.pop('plant_names', [])  # Get the plant_names from validated data
        plant = Plant.objects.create(**validated_data)  # Create the plant object
        
        # Create PlantLocalName instances for each plant name provided
        for name_data in plant_name_data:
            PlantLocalName.objects.create(plant=plant, **name_data)
        
        return plant

    def update(self, instance, validated_data):
        # If the user is a contributor, ensure restricted fields like 'status' cannot be updated
        request = self.context.get('request')
        if request and request.user and not request.user.is_staff:
            validated_data.pop('status', None)  # Ensure status cannot be modified by contributors
        
        # Call the parent update method to update the instance
        return super().update(instance, validated_data)

class MedicinalPlantNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicinalPlantName
        fields = ['medicinal_plant_name_id', 'medicinal_plant', 'language', 'localName']

class MedicinalPlantSerializer(serializers.ModelSerializer):
    medicinal_plant_names = MedicinalPlantNameSerializer(many=True, read_only=True)
    plant = PlantSerializer()

    class Meta:
        model = MedicinalPlant
        fields = '__all__'

class ScientificClarificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScientificClarification
        fields = '__all__'

class PlantImageGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantImageGallery
        fields = '__all__'

class MedicinalPlantImageGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicinalPlantImageGallery
        fields = '__all__'

class PlantVideoGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantVideoGallery
        fields = '__all__'
