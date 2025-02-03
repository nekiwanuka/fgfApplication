from django.contrib import admin
from .models import Plant, MedicinalPlant, PlantLocalName, Language, MedicinalPlantName, ScientificClarification, PlantImageGallery, MedicinalPlantImageGallery, PlantVideoGallery

@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ('plant_id', 'scientific_name', 'english_name', 'contributor', 'date_added')
    search_fields = ['scientific_name', 'english_name']

@admin.register(MedicinalPlant)
class MedicinalPlantAdmin(admin.ModelAdmin):
    list_display = ('medicinal_plant_id', 'plant', 'contributor')
    search_fields = ['plant__scientific_name', 'plant__english_name']

@admin.register(PlantLocalName)
class PlantNameAdmin(admin.ModelAdmin):
    list_display = ('plant', 'language', 'LocalName')
    search_fields = ['LocalName']

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('language_id', 'name')
    search_fields = ['name']

@admin.register(MedicinalPlantName)
class MedicinalPlantNameAdmin(admin.ModelAdmin):
    list_display = ('medicinal_plant', 'language', 'localName')
    search_fields = ['localName']

@admin.register(ScientificClarification)
class ScientificClarificationAdmin(admin.ModelAdmin):
    list_display = ('scientific_clarification_id', 'kingdom', 'order', 'family', 'genus', 'species')
    search_fields = ['species']

@admin.register(PlantImageGallery)
class PlantImageGalleryAdmin(admin.ModelAdmin):
    list_display = ('plant', 'caption')
    search_fields = ['plant__english_name']

@admin.register(MedicinalPlantImageGallery)
class MedicinalPlantImageGalleryAdmin(admin.ModelAdmin):
    list_display = ('medicinal_plant', 'caption')
    search_fields = ['medicinal_plant__plant__english_name']

@admin.register(PlantVideoGallery)
class PlantVideoGalleryAdmin(admin.ModelAdmin):
    list_display = ('plant', 'caption')
    search_fields = ['plant__english_name']