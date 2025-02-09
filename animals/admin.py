from django.contrib import admin
from .models import AnimalClassification, AnimalProfile, AnimalLocalName, EntryCounter

@admin.register(AnimalClassification)
class AnimalClassificationAdmin(admin.ModelAdmin):
    list_display = ('animal_classification_id', 'animal_class', 'kingdom_name', 'species', 'number_of_species', 'status', 'created_at')
    search_fields = ('animal_class', 'kingdom_name', 'species')
    list_filter = ('status', 'kingdom_name', 'domestic', 'wild_animal')
    readonly_fields = ('created_at', 'updated_at', 'published_date')

@admin.register(AnimalProfile)
class AnimalProfileAdmin(admin.ModelAdmin):
    list_display = ('animal_id', 'english_name', 'scientific_name', 'animal_classifications', 'conservation_status', 'status', 'created_at')
    search_fields = ('english_name', 'scientific_name', 'conservation_status')
    list_filter = ('status', 'conservation_status', 'habitat_impact')
    readonly_fields = ('created_at', 'updated_at', 'published_date')

@admin.register(AnimalLocalName)
class AnimalLocalNameAdmin(admin.ModelAdmin):
    list_display = ('animal_local_name_id', 'local_name', 'language', 'animal')
    search_fields = ('local_name', 'language', 'animal__english_name')
    list_filter = ('language',)
    
@admin.register(EntryCounter)
class EntryCounterAdmin(admin.ModelAdmin):
    list_display = ('model_name', 'total_entries')
    readonly_fields = ('model_name', 'total_entries')
