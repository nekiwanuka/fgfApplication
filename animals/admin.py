from django.contrib import admin
from .models import AnimalClassification, AnimalProfile, AnimalLocalName, EntryCounter
from django.contrib.auth.models import User


class AnimalClassificationAdmin(admin.ModelAdmin):
    list_display = ('kingdom_name', 'species', 'animal_class', 'order', 'domestic', 'wild_animal', 'number_of_species')
    search_fields = ('kingdom_name', 'species', 'animal_class', 'order')
    list_filter = ('domestic', 'wild_animal', 'animal_class')
    ordering = ('kingdom_name',)

class AnimalProfileAdmin(admin.ModelAdmin):
    list_display = ('english_name', 'scientific_name', 'status', 'date_entered', 'animal_classifications')
    search_fields = ('english_name', 'scientific_name', 'description', 'areas_in_Uganda')
    list_filter = ('status', 'animal_classifications')
    ordering = ('date_entered',)

class AnimalLocalNameAdmin(admin.ModelAdmin):
    list_display = ('local_name', 'language', 'animal', 'contributor')
    search_fields = ('local_name', 'language', 'animal__english_name', 'animal__scientific_name')
    list_filter = ('language',)
    ordering = ('animal', 'language')

class EntryCounterAdmin(admin.ModelAdmin):
    list_display = ('model_name', 'total_entries')
    search_fields = ('model_name',)
    ordering = ('model_name',)

# Register the models with custom admin
admin.site.register(AnimalClassification, AnimalClassificationAdmin)
admin.site.register(AnimalProfile, AnimalProfileAdmin)
admin.site.register(AnimalLocalName, AnimalLocalNameAdmin)
admin.site.register(EntryCounter, EntryCounterAdmin)

