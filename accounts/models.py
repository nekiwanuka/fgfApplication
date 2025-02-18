from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from fgfplatform import settings

# Custom User Manager
class FgfUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        # Ensure email is provided
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)

        # All new users are contributors but inactive until they verify email
        extra_fields.setdefault('is_contributor', True)
        extra_fields.setdefault('is_active', False)  # Must verify email to activate

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # Set default fields for superuser
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)  # Superusers are active by default
        return self.create_user(email, password, **extra_fields)

    def create_editor(self, email, password=None, **extra_fields):
        # Set default fields for editor
        extra_fields.setdefault('is_editor', True)
        extra_fields.setdefault('is_active', True)  # Editors are active by default
        return self.create_user(email, password, **extra_fields)

# Custom User Model
class FgfUser(AbstractUser):
    username = None  # Disabling the username field, using email for authentication
    email = models.EmailField(unique=True, db_index=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField(null=True, blank=True)
    deleted = models.BooleanField(default=False)

    # Gender choices for the user
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    
    # User Role Flags
    is_editor = models.BooleanField(default=False)
    is_contributor = models.BooleanField(default=True)

    objects = FgfUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Email is used for authentication, so no need for username

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.email} ({self.first_name} {self.last_name})"

    def promote_to_editor(self):
        """Promote a contributor to an editor."""
        self.is_editor = True
        self.is_contributor = False
        self.save()

    def promote_to_superuser(self):
        """Promote an editor to a superuser."""
        self.is_superuser = True
        self.is_editor = False
        self.is_staff = True
        self.save()


class UserProfile(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="user_profile", null=True
    )
    proffession = models.CharField(max_length=100)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.email} - UserProfile'
