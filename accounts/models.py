from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# Custom User Manager
class FgfUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)  # Ensure superuser is active by default
        return self.create_user(email, password, **extra_fields)

    def create_editor(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_editor', True)
        extra_fields.setdefault('is_active', True)  # Editors are active by default
        return self.create_user(email, password, **extra_fields)

    def create_contributor(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_contributor', True)
        extra_fields.setdefault('is_active', True)  # Contributors are active by default
        return self.create_user(email, password, **extra_fields)


# Custom User Model
class FgfUser(AbstractUser):
    username = None  # Disabling the username field, using email for authentication
    email = models.EmailField(unique=True, db_index=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField(null=True, blank=True)
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    
    # User Role Flags
    is_editor = models.BooleanField(default=False)
    is_contributor = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    

    objects = FgfUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Email is used for authentication, so no need for username

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.email} ({self.first_name} {self.last_name})"