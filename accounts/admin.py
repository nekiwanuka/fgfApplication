from django.contrib import admin
from .models import FgfUser, UserProfile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

@admin.register(FgfUser)
class FgfUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = FgfUser
    list_display = ('email', 'first_name', 'last_name', 'date_of_birth', 'gender', 'location', 'phone_number', 'is_editor', 'is_contributor', 'is_active', 'is_verified')
    list_filter = ('gender', 'location', 'is_editor', 'is_contributor', 'is_active', 'is_verified')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'date_of_birth', 'gender', 'location', 'phone_number')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_editor', 'is_contributor', 'is_verified')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'proffession')
    search_fields = ('user__email', 'proffession')
    list_filter = ('proffession',)