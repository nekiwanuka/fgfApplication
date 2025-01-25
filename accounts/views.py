from django.shortcuts import redirect, render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, viewsets
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import FgfUser
from .serializers import UserSerializer, ContributorRegistrationSerializer
from rest_framework.decorators import action
from django.contrib.sites.shortcuts import get_current_site
from django.views import View
from django.http import HttpResponse
from rest_framework.permissions import IsAdminUser


# Utility to send verification email
def send_verification_email(request, user):
    token = default_token_generator.make_token(user)  # Use Django's default token generator
    relative_link = reverse('verify-email', args=[user.pk, token])
    domain = get_current_site(request).domain
    full_link = f"http://{domain}{relative_link}"

    # Email content
    subject = "Verify Your Email Address"
    message = f"""
    Hi {user.first_name},

    Please verify your email address by clicking the link below:
    {full_link}

    Thank you!
    """
    user.email_user(subject, message)

# User ViewSet
class UserViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        if request.user.is_superuser:
            users = FgfUser.objects.filter(is_active=True)
        elif request.user.is_editor:
            users = FgfUser.objects.filter(is_active=True, is_contributor=True)
        else:
            return Response({"error": "You must be a superuser or editor to view users."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], permission_classes=[IsAdminUser | permissions.IsAuthenticated])
    def create_editor(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"error": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = FgfUser.objects.create_user(email=email, password=password, is_editor=True)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], permission_classes=[IsAdminUser | permissions.IsAuthenticated])
    def create_contributor(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"error": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = FgfUser.objects.create_user(email=email, password=password, is_contributor=True)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list_contributors(self, request):
        contributors = FgfUser.objects.filter(is_contributor=True, is_verified=True)
        serializer = UserSerializer(contributors, many=True)
        return Response(serializer.data)

    def list_editors(self, request):
        editors = FgfUser.objects.filter(is_editor=True)
        serializer = UserSerializer(editors, many=True)
        return Response(serializer.data)

# Email Verification View
class VerifyEmailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, user_id, token, *args, **kwargs):
        try:
            user = FgfUser.objects.get(pk=user_id)
        except FgfUser.DoesNotExist:
            return Response({'detail': 'Invalid user.'}, status=status.HTTP_400_BAD_REQUEST)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.is_verified = True  # Mark user as verified
            user.save()
            return redirect('login')  # Redirect to login after successful email verification
        return Response({'detail': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)

# Password Reset Verification View
class PasswordResetVerifyView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        uidb64 = kwargs.get('uidb64')
        token = kwargs.get('token')

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_user_model().objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                return redirect('password_reset_confirm', uidb64=uidb64, token=token)

            return Response({'detail': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception:
            return Response({'detail': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)

# Contributor Registration View
class ContributorRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = ContributorRegistrationSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            user = serializer.save()
            # Send verification email after user is saved
            send_verification_email(request, user)
            return Response({'detail': 'Registration successful. Please check your email for verification instructions.'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Authentication Views
class LoginView(TokenObtainPairView):
    pass

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')

        if not refresh_token:
            return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Blacklist the token
            token = RefreshToken(refresh_token)
            token.blacklist()

            # Return a 200 OK status with a success message
            return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

# Password Change Views
class PasswordChangeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)
        return Response({"error": "Old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailRedirectView(View):
    def get(self, request, *args, **kwargs):
        # Logic to verify the email
        # ...existing verification logic...
        return redirect('login')

def verify_email(request, user_id, token):
    user = get_object_or_404(FgfUser, pk=user_id)
    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Email verified successfully.')
    else:
        return HttpResponse('Invalid verification link.', status=400)
