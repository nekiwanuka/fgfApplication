from rest_framework import serializers
from accounts.models import FgfUser
from .models import (
    Plant, PlantLocalName, Language, MedicinalPlant, PlantImageGallery,
    PlantVideoGallery, PlantScientificClassification
)
from django.contrib.auth import get_user_model

class SimpleContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [ "first_name", "last_name"]
        

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ["name"]

class PlantScientificClassificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantScientificClassification
        fields = "__all__"

class PlantSerializer(serializers.ModelSerializer):
    contributor = SimpleContributorSerializer(read_only=True)
    contributor_id = serializers.PrimaryKeyRelatedField(
        source='contributor', queryset=FgfUser.objects.all(), write_only=True
    )
    plant_scientific_classification = PlantScientificClassificationSerializer(read_only=True)
    plant_scientific_classification_id = serializers.PrimaryKeyRelatedField(
        queryset=PlantScientificClassification.objects.all(),
        source="plant_scientific_classification",
        write_only=True
    )
    
    class Meta:
        model = Plant
        fields = "__all__"
        read_only_fields = ['citation', 'created_at', 'updated_at', 'review_feedback', 'status', 'published_date']

class PlantLocalNameSerializer(serializers.ModelSerializer):
    plant = PlantSerializer(read_only=True)
    plant_id = serializers.PrimaryKeyRelatedField(
        queryset=Plant.objects.all(), source='plant', write_only=True
    )
    language = LanguageSerializer(read_only=True)
    language_id = serializers.PrimaryKeyRelatedField(
        queryset=Language.objects.all(), source='language', write_only=True
    )
    
    class Meta:
        model = PlantLocalName
        fields = [ "plant", "plant_id", "language", "language_id", "local_name"]

    def create(self, validated_data):
        plant = validated_data["plant"]
        language = validated_data["language"]
        local_name = validated_data["local_name"]
        existing_entry = PlantLocalName.objects.filter(
            plant=plant, language=language, local_name=local_name
        ).exists()
        if existing_entry:
            raise serializers.ValidationError("This local name already exists for this plant in the given language.")
        return super().create(validated_data)

class MedicinalPlantSerializer(serializers.ModelSerializer):
    plant = PlantSerializer(read_only=True)
    plant_id = serializers.PrimaryKeyRelatedField(
        queryset=Plant.objects.all(), source='plant', write_only=True
    )
    
    class Meta:
        model = MedicinalPlant
        exclude = ['medicinal_plant_id'] 
        fields = "__all__"

class PlantImageGallerySerializer(serializers.ModelSerializer):
    plant = PlantSerializer(read_only=True)
    plant_id = serializers.PrimaryKeyRelatedField(
        queryset=Plant.objects.all(), source='plant', write_only=True
    )
    
    class Meta:
        model = PlantImageGallery
        fields = "__all__"

class PlantVideoGallerySerializer(serializers.ModelSerializer):
    plant = PlantSerializer(read_only=True)
    plant_id = serializers.PrimaryKeyRelatedField(
        queryset=Plant.objects.all(), source='plant', write_only=True
    )
    
    class Meta:
        model = PlantVideoGallery
        fields = "__all__"
