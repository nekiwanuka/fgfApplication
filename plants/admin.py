from django.contrib import admin
from .models import (
    PlantScientificClassification, Plant, Language, PlantLocalName, MedicinalPlant, 
    PlantImageGallery, PlantVideoGallery, PlantEntryCounter
)
from unfold.admin import ModelAdmin 

@admin.register(PlantScientificClassification)
class scientificClassificationAdmin(ModelAdmin):
    list_display = ("kingdom", "order", "family", "genus", "species")
    search_fields = ("kingdom", "order", "family", "genus", "species")

@admin.register(Plant)
class PlantAdmin(ModelAdmin):
    list_display = ("english_name", "scientific_name", "life_form", "status", "contributor")
    search_fields = ("english_name", "scientific_name", "distribution_in_uganda")
    list_filter = ("life_form", "status", "created_at")
    autocomplete_fields = ["plant_scientific_classification", "contributor"]
    ordering = ['english_name'] 
    readonly_fields = ('created_at', 'updated_at', 'published_date')

@admin.register(Language)
class LanguageAdmin(ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(PlantLocalName)
class PlantLocalNameAdmin(ModelAdmin):
    list_display = ("plant", "language", "local_name")
    search_fields = ("plant__english_name", "local_name")
    list_filter = ("language",)

@admin.register(MedicinalPlant)
class MedicinalPlantAdmin(ModelAdmin):
    list_display = ("plant", "part_used", "status", "contributor")
    search_fields = ("plant__english_name", "health_issues", "cultural_value")
    list_filter = ("status", "created_at")
    autocomplete_fields = ("plant", "contributor")

@admin.register(PlantImageGallery)
class PlantImageGalleryAdmin(ModelAdmin):
    list_display = ("plant", "caption")
    search_fields = ("plant__english_name", "caption")

@admin.register(PlantVideoGallery)
class PlantVideoGalleryAdmin(ModelAdmin):
    list_display = ("plant", "caption")
    search_fields = ("plant__english_name", "caption")



@admin.register(PlantEntryCounter)
class PlantEntryCounterAdmin(ModelAdmin):
    list_display = ("model_name", "total_entries")
    search_fields = ("model_name",)
