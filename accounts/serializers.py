from rest_framework import serializers
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.core.mail import send_mail, BadHeaderError
from django.core.exceptions import ValidationError
import re
from .models import FgfUser

# Utility function for sending emails
def send_email(recipient_email, subject, message):
    try:
        send_mail(subject, message, 'no-reply@example.com', [recipient_email])
    except BadHeaderError:
        raise serializers.ValidationError("Invalid header found.")
    except Exception as e:
        raise serializers.ValidationError(f"An error occurred while sending the email: {str(e)}")

# Phone number validation
def validate_phone_number(value):
    phone_regex = r'^\+?1?\d{9,15}$'  # Simple regex for validating international phone numbers
    if not re.match(phone_regex, value):
        raise ValidationError("Invalid phone number format.")
    return value

# Registration Serializer for Contributors
class ContributorRegistrationSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(validators=[validate_phone_number])
    
    class Meta:
        model = FgfUser
        fields = (
            'id', 'email', 'password', 'first_name', 'last_name', 'date_of_birth',
            'gender', 'location', 'phone_number', 'is_contributor', 'is_active',
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Ensure password is hashed
        validated_data['is_contributor'] = True
        user = FgfUser.objects.create_user(**validated_data)
        user.is_active = False  # Ensure the user is inactive until verification
        user.save()
        self.send_verification_email(user)
        return user

    def send_verification_email(self, user):
        token = default_token_generator.make_token(user)
        verification_url = self.context['request'].build_absolute_uri(
            reverse('verify_email', args=[user.pk, token])
        )
        subject = 'Verify Your Email Address'
        message = (
            f'Hi {user.first_name},\n\n'
            f'Please verify your email address by clicking the link below:\n'
            f'{verification_url}\n\n'
            f'Thank you!'
        )
        send_email(user.email, subject, message)

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FgfUser
        fields = [
            'id', 'email', 'first_name', 'last_name', 'date_of_birth', 'gender',
            'location', 'phone_number', 'is_editor', 'is_contributor', 'is_active',
        ]


# Custom User Serializer
class FgfUserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(validators=[validate_phone_number])

    class Meta:
        model = FgfUser
        fields = [
            'id', 'email', 'first_name', 'last_name', 'date_of_birth', 'gender',
            'location', 'phone_number', 'is_editor', 'is_contributor', 'is_active',
        ]
