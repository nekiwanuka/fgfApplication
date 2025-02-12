from rest_framework import serializers
from accounts.models import FgfUser
from .models import AnimalProfile, AnimalClassification, AnimalLocalName, AnimalEntryCounter, AnimalImageGallery, AnimalVideoGallery

# ✅ Contributor Serializer (Handles a Single Contributor)
class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = FgfUser
        fields = ['id', 'first_name', 'last_name', 'email']


# ✅ Full Animal Classification Serializer (For Direct Use)
class AnimalClassificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalClassification
        fields = '__all__'


# ✅ Nested Animal Classification Serializer (For Use Inside AnimalProfile)
class AnimalClassificationNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalClassification
        fields = [
            "kingdom",
            "phylum",
            "animal_class",
            "order",
            "family",
            "genus",
            "species",
            "number_of_species",
        ]  # Only keep essential fields for nested use


# ✅ Animal Profile Serializer
class AnimalProfileSerializer(serializers.ModelSerializer):
    animal_classification_details = AnimalClassificationNestedSerializer(source='animal_classification', read_only=True)

    # Single contributor (ForeignKey)
    contributor = ContributorSerializer(read_only=True)
    contributor_id = serializers.PrimaryKeyRelatedField(
        source='contributor', queryset=FgfUser.objects.all(), write_only=True
    )

    class Meta:
        model = AnimalProfile
        fields = '__all__'
        read_only_fields = ['citation', 'created_at', 'updated_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # ✅ Exclude classification details if empty
        if not representation.get('animal_classification_details'):
            representation.pop('animal_classification_details', None)

        return representation


# ✅ Animal Local Name Serializer
class AnimalLocalNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalLocalName
        fields = '__all__'
        
class AnimalImageGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalImageGallery
        fields = '__all__'
        
class AnimalVideoGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalVideoGallery
        fields = '__all__'


# ✅ Entry Counter Serializer
class EntryCounterSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalEntryCounter
        fields = '__all__'
        read_only_fields = ['model_name', 'total_entries']
