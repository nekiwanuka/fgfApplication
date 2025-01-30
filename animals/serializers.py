from rest_framework import serializers
from .models import AnimalClassification, AnimalProfile, AnimalLocalName, AnimalEntryCounter
from accounts.models import FgfUser

class FgfUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FgfUser
        fields = ['id', 'email', 'first_name', 'last_name']
        ref_name = 'AnimalsFgfUser'  # Add this line to set a unique ref_name

class AnimalClassificationSerializer(serializers.ModelSerializer):
    contributors = FgfUserSerializer(many=True, read_only=True)

    class Meta:
        model = AnimalClassification
        fields = '__all__'

class AnimalLocalNameSerializer(serializers.ModelSerializer):
    contributor = FgfUserSerializer(read_only=True)
    animal = serializers.PrimaryKeyRelatedField(queryset=AnimalProfile.objects.all())

    class Meta:
        model = AnimalLocalName
        fields = '__all__'

class AnimalProfileSerializer(serializers.ModelSerializer):
    contributors = FgfUserSerializer(many=True, read_only=True)
    animal_classifications = AnimalClassificationSerializer(read_only=True)
    local_names = AnimalLocalNameSerializer(many=True, read_only=True)

    class Meta:
        model = AnimalProfile
        fields = '__all__'

# For creating/updating local names
class AnimalLocalNameCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalLocalName
        fields = ['animal', 'local_name', 'language']

class AnimalEntryCounterSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalEntryCounter
        fields = ['id', 'total_entries']
