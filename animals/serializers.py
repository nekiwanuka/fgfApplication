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
        read_only_fields = ['review_feedback', 'citation', 'created_at', 'updated_at']
        extra_kwargs = {'contributors': {'read_only': True}}  # Ensure contributors can't be modified directly

    def is_contributor(self):
        """Check if the user is authenticated and NOT staff."""
        request = self.context.get('request', None)
        user = getattr(request, 'user', None)
        return user and user.is_authenticated and not user.is_staff

    def to_representation(self, instance):
        """Customize response to exclude 'status' field for contributors."""
        representation = super().to_representation(instance)
        if self.is_contributor():
            representation.pop('status', None)  # Hide 'status' for contributors
        return representation

    def update(self, instance, validated_data):
        """Prevent contributors from modifying the 'status' field."""
        if self.is_contributor():
            validated_data.pop('status', None)  # Remove status from update data
        return super().update(instance, validated_data)

    def create(self, validated_data):
        """Ensure 'status' defaults to 'draft' and add the contributor."""
        request = self.context.get('request')  # Get request context
        validated_data.setdefault('status', 'draft')  # Default status to draft
            
        animal_profile = super().create(validated_data)  # Create the object
            
        if request and request.user.is_authenticated:
            animal_profile.contributor.add(request.user)  # Add the logged-in user as a contributor

        contributors = validated_data.pop('contributor', [])
        if contributors:
            animal_profile.contributor.set(contributors)

        return animal_profile





class AnimalLocalNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalLocalName
        fields = '__all__'


class EntryCounterSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntryCounter
        fields = '__all__'
