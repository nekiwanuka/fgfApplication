from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserViewSet, LoginView, LogoutView, PasswordChangeView, VerifyEmailView,
    ContributorRegistrationView, PasswordResetVerifyView, VerifyEmailRedirectView, UserProfileView,
    FgfUserListCreateView, FgfUserDetailView, ProfileListCreateView, ProfileDetailView
)

# Router setup for UserViewSet
router = DefaultRouter()
router.register('users', UserViewSet, basename='user')

# Authentication and User Management URLs
auth_patterns = [
    path('auth/login/', LoginView.as_view(), name='login'),
    path('login/', LoginView.as_view(), name='login_page'),  # Added this line
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/signup/', ContributorRegistrationView.as_view(), name='signup'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/password/change/', PasswordChangeView.as_view(), name='password_change'),
    path('auth/profile/', UserProfileView.as_view(), name='profile'),
]

# Email Verification URLs
email_verification_patterns = [
    path('auth/verify-email/<int:user_id>/<str:token>/', VerifyEmailView.as_view(), name='verify_email'),  # Updated this line
    path('auth/verify-email-redirect/', VerifyEmailRedirectView.as_view(), name='verify_email_redirect'),
]

# Password Reset URLs
password_reset_patterns = [
    path('auth/password-reset-verify/<str:uidb64>/<str:token>/', PasswordResetVerifyView.as_view(), name='password_reset_verify'),
]

# FgfUser and Profile URLs
fgf_user_profile_patterns = [
    path('users/', FgfUserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', FgfUserDetailView.as_view(), name='user-detail'),
    path('userprofiles/', ProfileListCreateView.as_view(), name='user-profile-list-create'),
    path('userprofiles/<int:pk>/', ProfileDetailView.as_view(), name='user-profile-detail'),
]

# Combine all URL patterns
urlpatterns = [
    path('', include(router.urls)),  # UserViewSet endpoints
    *auth_patterns,
    *email_verification_patterns,
    *password_reset_patterns,
    *fgf_user_profile_patterns,
]