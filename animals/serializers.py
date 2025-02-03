from rest_framework import serializers
from .models import AnimalProfile, AnimalClassification, AnimalLocalName, EntryCounter

class AnimalClassificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalClassification
        fields = '__all__'


class AnimalProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalProfile
        fields = '__all__'


class AnimalLocalNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalLocalName
        fields = '__all__'


class EntryCounterSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntryCounter
        fields = '__all__'
