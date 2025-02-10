from django.conf import settings

from django.db import models

from fgfplatform.constants import STATUS_CHOICES


LIFE_FORM_CHOICES = [
    ("forest", "Forest"),
    ("meadow", "Meadow"),
    ("climber", "Climber"),
    ("grassland", "Grassland"),
    ("herb", "Herb"),
    ("shrub", "Shrub"),
    ("tree", "Tree"),
    ("perennial", "Perennial"),
    ("vine", "Vine"),
    ("water", "Water"),
    ("tender", "Tender"),
    ("other", "Other"),
]



class ScientificClassification(models.Model):
    kingdom = models.CharField(max_length=100, blank=True, null=True)
    order = models.CharField(max_length=100, blank=True, null=True)
    family = models.CharField(max_length=100, blank=True, null=True)
    genus = models.CharField(max_length=100, blank=True, null=True)
    species = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.kingdom} {self.order} {self.family} {self.genus} {self.species}"

class Plant(models.Model):
    scientific_name = models.CharField(max_length=100, unique=True, blank=True, null=True)
    synonyms = models.TextField(max_length=255, blank=True, null=True)
    english_name = models.CharField(max_length=100, unique=True, blank=True, null=True)
    scientific_classification = models.ForeignKey(ScientificClassification, on_delete=models.SET_NULL, null=True, blank=True
    )
    distribution_in_uganda = models.CharField(max_length=100, blank=True, null=True)
    unique_habitat = models.CharField(max_length=100, blank=True, null=True)
    life_form = models.CharField(max_length=100, choices=LIFE_FORM_CHOICES, null=True)
    life_span = models.CharField(max_length=100, blank=True, null=True)
    climate_impact = models.CharField(max_length=100, blank=True, null=True)
    threats = models.CharField(max_length=100, blank=True, null=True)
    toxicity = models.CharField(max_length=100, blank=True, null=True)
    conservation_status = models.CharField(max_length=100, blank=True, null=True)
    known_values = models.TextField()
    image = models.ImageField(upload_to="plant_images/", blank=True, null=True)
    video = models.FileField(upload_to="plant_videos/", blank=True, null=True)
    audio = models.FileField(upload_to="plant_audio/", blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    citation = models.CharField(max_length=255)
    contributor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="plants", null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    review_feedback = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(blank=True, null=True)
   
    def __str__(self):
        return f"Plant: {self.english_name or self.scientific_name}"

class Language(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class PlantLocalName(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name="local_names")
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    local_name = models.CharField(max_length=255)

    class Meta:
        unique_together = ("plant", "language", "local_name")

    def __str__(self):
        return f"{self.local_name} ({self.language})"

class MedicinalPlant(models.Model):
    plant = models.OneToOneField(Plant, on_delete=models.CASCADE, related_name="medicinal_info")
    health_issues = models.TextField()
    part_used = models.CharField(max_length=100, blank=True, null=True)
    preparation_steps = models.TextField()
    dosage = models.CharField(max_length=100, blank=True, null=True)
    contraindications = models.TextField()
    shelf_life = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    cultural_value = models.TextField(blank=True, null=True)
    contributor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="medicinal_plants", null=True
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    review_feedback = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return f"Medicinal Info for {self.plant.english_name}"

class PlantImageGallery(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name="image_gallery")
    image = models.ImageField(upload_to="plant_gallery/", blank=True, null=True)
    caption = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Image: {self.caption} ({self.plant.english_name})"

class PlantVideoGallery(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name="video_gallery")
    video = models.FileField(upload_to="plant_videos/", blank=True, null=True)
    caption = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Video: {self.caption} ({self.plant.english_name})"




class PlantEntryCounter(models.Model):
    model_name = models.CharField(max_length=100, unique=True)
    total_entries = models.PositiveIntegerField(default=0)

    def increment(self):
        self.total_entries += 1
        self.save()

    def decrement(self):
        if self.total_entries > 0:
            self.total_entries -= 1
            self.save()

    def __str__(self):
        return f"{self.model_name} Total Entries: {self.total_entries}"
