from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import FgfUser

# Custom User Admin
class FgfUserAdmin(UserAdmin):
    model = FgfUser
    list_display = (
        'email', 'first_name', 'last_name', 'is_contributor', 'is_editor', 'is_active', 'is_verified', 'date_of_birth', 'phone_number'
    )
    list_filter = ('is_contributor', 'is_editor', 'is_active', 'is_verified')
    search_fields = ('email', 'first_name', 'last_name', 'phone_number')
    ordering = ('email',)
    
    # Fields to display in the add and change forms
    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'date_of_birth', 'gender', 'location', 'phone_number')
        }),
        ('Permissions', {
            'fields': ('is_contributor', 'is_editor', 'is_active', 'is_verified', 'is_superuser')
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'date_of_birth', 'gender', 'location', 'phone_number')
        }),
        ('Permissions', {
            'fields': ('is_contributor', 'is_editor', 'is_active', 'is_verified', 'is_superuser')
        }),
    )
    filter_horizontal = ()
    list_per_page = 25

# Register the custom admin class
admin.site.register(FgfUser, FgfUserAdmin)
