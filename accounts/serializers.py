from rest_framework import serializers
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.core.mail import send_mail, BadHeaderError
from .models import CustomUser


# Registration Serializer for Contributors

class ContributorRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'id', 'email', 'password', 'first_name', 'last_name', 'date_of_birth', 
            'gender', 'location', 'phone_number', 'is_contributor', 'is_active',
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['is_contributor'] = True
        user = CustomUser.objects.create_user(**validated_data)
        self.send_verification_email(user)
        return user

    def send_verification_email(self, user):
        # Generate the email verification URL
        token = default_token_generator.make_token(user)
        verification_url = self.build_verification_url(user, token)
        
        # Send the email
        subject = 'Verify Your Email Address'
        message = f'Hi {user.first_name},\n\nPlease verify your email address by clicking the link below:\n{verification_url}\n\nThank you!'
        
        self.send_email(user.email, subject, message)

    def build_verification_url(self, user, token):
        return self.context['request'].build_absolute_uri(
            reverse('verify_email', args=[user.pk, token])
        )

    def send_email(self, recipient_email, subject, message):
        try:
            send_mail(subject, message, 'no-reply@example.com', [recipient_email])
        except BadHeaderError:
            raise serializers.ValidationError("Invalid header found.")
        except Exception as e:
            raise serializers.ValidationError(f"An error occurred while sending the email: {str(e)}")


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', 'email', 'first_name', 'last_name', 'date_of_birth', 'gender',
            'location', 'phone_number', 'is_editor', 'is_contributor', 'is_active'
        ]

# Custom User Serializer
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', 'email', 'first_name', 'last_name', 'date_of_birth', 'gender',
            'location', 'phone_number', 'is_editor', 'is_contributor', 'is_active'
        ]

# Registration Serializer for Contributors
class ContributorRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'id', 'email', 'password', 'first_name', 'last_name', 'date_of_birth', 
            'gender', 'location', 'phone_number', 'is_contributor', 'is_active',
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['is_contributor'] = True
        user = CustomUser.objects.create_user(**validated_data)
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
        try:
            send_mail(subject, message, 'no-reply@example.com', [user.email])
        except BadHeaderError:
            raise serializers.ValidationError("Invalid header found.")
        except Exception as e:
            raise serializers.ValidationError(f"An error occurred while sending the email: {str(e)}")
