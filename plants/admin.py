from django.contrib import admin
from .models import (
    ScientificClassification, Plant, Language, PlantLocalName, MedicinalPlant, 
    PlantImageGallery, PlantVideoGallery, PlantEntryCounter
)

@admin.register(ScientificClassification)
class scientificClassificationAdmin(admin.ModelAdmin):
    list_display = ("kingdom", "order", "family", "genus", "species")
    search_fields = ("kingdom", "order", "family", "genus", "species")

@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ("english_name", "scientific_name", "life_form", "status", "contributor")
    search_fields = ("english_name", "scientific_name", "distribution_in_uganda")
    list_filter = ("life_form", "status", "created_at")
    autocomplete_fields = ["scientific_classification", "contributor"]
    ordering = ['english_name'] 

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(PlantLocalName)
class PlantLocalNameAdmin(admin.ModelAdmin):
    list_display = ("plant", "language", "local_name")
    search_fields = ("plant__english_name", "local_name")
    list_filter = ("language",)

@admin.register(MedicinalPlant)
class MedicinalPlantAdmin(admin.ModelAdmin):
    list_display = ("plant", "part_used", "status", "contributor")
    search_fields = ("plant__english_name", "health_issues", "cultural_value")
    list_filter = ("status", "created_at")
    autocomplete_fields = ("plant", "contributor")

@admin.register(PlantImageGallery)
class PlantImageGalleryAdmin(admin.ModelAdmin):
    list_display = ("plant", "caption")
    search_fields = ("plant__english_name", "caption")

@admin.register(PlantVideoGallery)
class PlantVideoGalleryAdmin(admin.ModelAdmin):
    list_display = ("plant", "caption")
    search_fields = ("plant__english_name", "caption")



@admin.register(PlantEntryCounter)
class PlantEntryCounterAdmin(admin.ModelAdmin):
    list_display = ("model_name", "total_entries")
    search_fields = ("model_name",)
