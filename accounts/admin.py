from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import AdminPasswordChangeForm  # Import this
from unfold.admin import ModelAdmin  # Use Unfold ModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget
from django.db import models
from .models import FgfUser, UserProfile

@admin.register(FgfUser)
class FgfUserAdmin(ModelAdmin, UserAdmin):  # Keep Unfold styling
    add_form = UserCreationForm
    form = UserChangeForm
    change_password_form = AdminPasswordChangeForm  # Ensure password UI is styled correctly
    model = FgfUser

    list_display = ('email', 'first_name', 'last_name', 'date_of_birth', 'gender', 'location', 'phone_number', 'is_editor', 'is_contributor', 'is_active', 'is_verified')
    list_filter = ('gender', 'location', 'is_editor', 'is_contributor', 'is_active', 'is_verified')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),  # Django will handle password styling
        ('Personal info', {'fields': ('first_name', 'last_name', 'date_of_birth', 'gender', 'location', 'phone_number')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_editor', 'is_contributor', 'is_verified')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'is_editor', 'is_contributor', 'is_verified')},
        ),
    )

    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

@admin.register(UserProfile)
class UserProfileAdmin(ModelAdmin):  # Using Unfold's ModelAdmin
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        }
    }
    list_display = ['user','proffession']  # Fixed typo
    search_fields = ['user__email']
    list_filter = ['proffession']
    