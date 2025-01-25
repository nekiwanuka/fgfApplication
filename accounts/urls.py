from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UserViewSet, LoginView, LogoutView, PasswordChangeView, VerifyEmailView, ContributorRegistrationView, PasswordResetVerifyView, VerifyEmailRedirectView
from . import views  # Add this import

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')

urlpatterns = [
    # Authentication URLs
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', ContributorRegistrationView.as_view(), name='signup'),
    path('auth/login/', LoginView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', LogoutView.as_view(), name='auth_logout'),
    path('auth/password/change/', PasswordChangeView.as_view(), name='auth_password_change'),

    # Email verification routes
    path('verify-email/<int:pk>/<str:token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('verify-email/<int:user_id>/<str:token>/', views.verify_email, name='verify_email'),

    path('verify-email-redirect/', VerifyEmailRedirectView.as_view(), name='verify-email-redirect'),

    # Password reset route
    path('password-reset-verify/<str:uidb64>/<str:token>/', PasswordResetVerifyView.as_view(), name='password_reset_verify'),

    # User view set (CRUD)
    path('', include(router.urls)),
]
