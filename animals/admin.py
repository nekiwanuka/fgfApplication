from django.contrib import admin
from .models import AnimalClassification, AnimalProfile, AnimalLocalName, AnimalEntryCounter


@admin.register(AnimalProfile)
class AnimalProfileAdmin(admin.ModelAdmin):
    list_display = ('english_name', 'scientific_name','pk','status', 'date_entered', 'animal_classifications','get_contributors')  # Removed 'id'
    search_fields = ('english_name', 'scientific_name', 'description')
    list_filter = ('status', 'date_entered')
    filter_horizontal = ('contributors',)
    def get_contributors(self, obj):
        return ", ".join([f"{contrib.first_name} {contrib.last_name} ({contrib.email})" for contrib in obj.contributors.all()])
    get_contributors.short_description = 'Contributors'


@admin.register(AnimalClassification)
class AnimalClassificationAdmin(admin.ModelAdmin):
    list_display = ('kingdom_name', 'get_contributors')  # Removed 'id'
    search_fields = ('kingdom_name', 'species', 'animal_class')
    ordering = ('kingdom_name',)

    def get_contributors(self, obj):
        return ", ".join([f"{contrib.first_name} {contrib.last_name} ({contrib.email})" for contrib in obj.contributors.all()])
    get_contributors.short_description = 'Contributors'


@admin.register(AnimalLocalName)
class AnimalLocalNameAdmin(admin.ModelAdmin):
    list_display = ('local_name', 'language', 'get_contributor')  # Removed 'id'
    search_fields = ('local_name', 'language')
    ordering = ('local_name',)

    def get_contributor(self, obj):
        if obj.contributor:
            return f"{obj.contributor.first_name} {obj.contributor.last_name} ({obj.contributor.email})"
        return "No Contributor"
    get_contributor.short_description = 'Contributor'



@admin.register(AnimalEntryCounter)
class AnimalEntryCounterAdmin(admin.ModelAdmin):
    list_display = ('id', 'total_entries')
    readonly_fields = ('total_entries',)

    def has_add_permission(self, request):
        # Limit to only one counter
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)
