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
        fields = ["id", "first_name", "last_name", "email"]

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ["id", "name"]

class PlantSerializer(serializers.ModelSerializer):
    contributor = SimpleContributorSerializer(read_only=True)
    contributor_id = serializers.PrimaryKeyRelatedField(
    source='contributor', queryset=FgfUser.objects.all(), write_only=True)
    class Meta:
        model = Plant
        fields = "__all__"
        read_only_fields = ['citation', 'created_at', 'updated_at','review_feedback', 'status', 'published_date']

class PlantLocalNameSerializer(serializers.ModelSerializer):
    plant = serializers.PrimaryKeyRelatedField(queryset=Plant.objects.all())
    language = serializers.PrimaryKeyRelatedField(queryset=Language.objects.all())

    class Meta:
        model = PlantLocalName
        fields = ["id", "plant", "language", "local_name"]

    def create(self, validated_data):
        """
        Ensures that new local names are added incrementally and existing ones are not overwritten.
        """
        plant = validated_data["plant"]
        language = validated_data["language"]
        local_name = validated_data["local_name"]

        # Check if the local name already exists for this plant-language combination
        existing_entry = PlantLocalName.objects.filter(plant=plant, language=language, local_name=local_name).exists()
        if existing_entry:
            raise serializers.ValidationError("This local name already exists for this plant in the given language.")

        return super().create(validated_data)

class MedicinalPlantSerializer(serializers.ModelSerializer):
    plant = serializers.PrimaryKeyRelatedField(queryset=Plant.objects.all())

    class Meta:
        model = MedicinalPlant
        fields = "__all__"

class PlantImageGallerySerializer(serializers.ModelSerializer):
    plant = serializers.PrimaryKeyRelatedField(queryset=Plant.objects.all())

    class Meta:
        model = PlantImageGallery
        fields = "__all__"

class PlantVideoGallerySerializer(serializers.ModelSerializer):
    plant = serializers.PrimaryKeyRelatedField(queryset=Plant.objects.all())

    class Meta:
        model = PlantVideoGallery
        fields = "__all__"


class PlantScientificClassificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantScientificClassification
        fields = "__all__"

class PlantScientificClassificationNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantScientificClassification
        fields = [
            "kingdom",
            "phylum",
            "animal_class",
            "order",
            "family",
            "genus",
            "species",
        ]