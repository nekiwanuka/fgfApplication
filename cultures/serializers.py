from rest_framework import serializers
from .models import EthnicGroup, Ethnicity, CulturalKingdom, Clan, ClanProfile

class EthnicGroupSerializer(serializers.ModelSerializer):
    """Returns all fields including contributor when fetched directly."""
    
    # Read-only fields
    citation = serializers.ReadOnlyField()
    status = serializers.ReadOnlyField()
    review_feedback = serializers.ReadOnlyField()
    date_created = serializers.ReadOnlyField()
    updated_at = serializers.ReadOnlyField()
    published_date = serializers.ReadOnlyField()

    class Meta:
        model = EthnicGroup
        fields = '__all__'  # Includes contributor

class EthnicGroupNestedSerializer(serializers.ModelSerializer):
    """Used when EthnicGroup is included in other models, excluding contributor fields."""
    class Meta:
        model = EthnicGroup
        exclude = ['contributor', 'primary_contributor']

class EthnicitySerializer(serializers.ModelSerializer):
    """Returns all fields including contributor when fetched directly."""
    ethnic_group = EthnicGroupSerializer(read_only=True)
    
    # Read-only fields
    citation = serializers.ReadOnlyField()
    status = serializers.ReadOnlyField()
    review_feedback = serializers.ReadOnlyField()
    date_created = serializers.ReadOnlyField()
    updated_at = serializers.ReadOnlyField()
    published_date = serializers.ReadOnlyField()

    class Meta:
        model = Ethnicity
        fields = '__all__'  # Includes contributor

class EthnicityNestedSerializer(serializers.ModelSerializer):
    """Used when Ethnicity is included in other models, excluding contributor fields."""
    ethnic_group = EthnicGroupNestedSerializer(read_only=True)
    
    class Meta:
        model = Ethnicity
        exclude = ['contributor', 'primary_contributor']

class CulturalKingdomSerializer(serializers.ModelSerializer):
    """Returns all fields including contributor when fetched directly."""
    ethnicity = EthnicitySerializer(read_only=True)
    
    # Read-only fields
    citation = serializers.ReadOnlyField()
    status = serializers.ReadOnlyField()
    review_feedback = serializers.ReadOnlyField()
    date_created = serializers.ReadOnlyField()
    updated_at = serializers.ReadOnlyField()
    published_date = serializers.ReadOnlyField()

    class Meta:
        model = CulturalKingdom
        fields = '__all__'  # Includes contributor

class CulturalKingdomNestedSerializer(serializers.ModelSerializer):
    """Used when CulturalKingdom is included in other models, excluding contributor fields."""
    ethnicity = EthnicityNestedSerializer(read_only=True)
    
    class Meta:
        model = CulturalKingdom
        exclude = ['contributor', 'primary_contributor']

class ClanSerializer(serializers.ModelSerializer):
    """Returns all fields for Clan, while nesting EthnicGroup, Ethnicity, and CulturalKingdom without contributors."""
    ethnicity = EthnicityNestedSerializer(read_only=True)
    cultural_kingdom = CulturalKingdomNestedSerializer(read_only=True)
    contributor = serializers.StringRelatedField()
    primary_contributor = serializers.StringRelatedField()

    # Read-only fields
    citation = serializers.ReadOnlyField()
    status = serializers.ReadOnlyField()
    review_feedback = serializers.ReadOnlyField()
    date_created = serializers.ReadOnlyField()
    updated_at = serializers.ReadOnlyField()
    published_date = serializers.ReadOnlyField()

    class Meta:
        model = Clan
        fields = '__all__'


class ClanProfileSerializer(serializers.ModelSerializer):
    ethnic_group = EthnicGroupNestedSerializer(read_only=True)
    cultural_kingdom = CulturalKingdomNestedSerializer(read_only=True)
    clan = ClanSerializer(read_only=True)  # Use the correct serializer to return full clan details
    editor = serializers.CharField(source="editor.username", read_only=True)  # Ensure editor's username is shown

    class Meta:
        model = ClanProfile
        fields = '__all__'  # Ensure all fields are included

