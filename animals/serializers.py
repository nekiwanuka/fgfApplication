from rest_framework import serializers
from .models import AnimalProfile, AnimalClassification, AnimalLocalName, EntryCounter

class AnimalClassificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalClassification
        fields = '__all__'


class AnimalProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalProfile
        fields = '__all__'  # Include all fields by default

    def to_representation(self, instance):
        # Get the original serialized data
        representation = super().to_representation(instance)
        
        # Get the request context (used to check user role)
        request = self.context.get('request')

        # If user is a contributor, hide the status field in the response
        if request and request.user and not request.user.is_staff:  # Contributor check
            representation.pop('status', None)  # Exclude the status field
        
        return representation

    def update(self, instance, validated_data):
        # If user is a contributor, remove the status field from the validated data
        request = self.context.get('request')
        if request and request.user and not request.user.is_staff:
            validated_data.pop('status', None)
        
        return super().update(instance, validated_data)

    def create(self, validated_data):
        # Ensure 'status' is set to a default value (e.g., 'draft') for new entries
        validated_data['status'] = 'draft'  # Automatically set 'status' to 'draft'
        return super().create(validated_data)



class AnimalLocalNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalLocalName
        fields = '__all__'


class EntryCounterSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntryCounter
        fields = '__all__'
