from django.db import models
from django.conf import settings  # Ensure correct reference to AUTH_USER_MODEL
from fgfplatform.constants import STATUS_CHOICES

# File Upload Path Helpers
def animal_media_upload_path(instance, filename):
    return f"animal_media/{instance.id}/{filename}"

class AnimalClassification(models.Model):
    animal_classification_id = models.AutoField(primary_key=True)
    kingdom = models.CharField(max_length=250, db_index=True)
    phylum = models.CharField(max_length=250, db_index=True)
    animal_class = models.CharField(max_length=250, db_index=True)
    order = models.CharField(max_length=250, db_index=True)
    family = models.CharField(max_length=250, db_index=True)
    genus = models.CharField(max_length=250, db_index=True)
    species = models.CharField(max_length=250, db_index=True)
    number_of_species = models.IntegerField(default=1, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    review_feedback = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.animal_class} ({self.kingdom})"

class AnimalProfile(models.Model):
    english_name = models.CharField(max_length=250, db_index=True)
    scientific_name = models.CharField(max_length=250, db_index=True)
    description = models.TextField(null=True, blank=True)
    areas_in_Uganda = models.CharField(max_length=250, blank=True, null=True)
    animal_classification = models.ForeignKey(
        AnimalClassification, 
        on_delete=models.SET_NULL,  # ✅ Set to NULL instead of deleting AnimalProfile
        null=True,
        blank=True
    )
    known_values = models.TextField(blank=True, null=True)
    value_details = models.TextField(blank=True, null=True)
    unique_habitat = models.CharField(max_length=250, blank=True, null=True)
    toxicity_to_humans = models.CharField(max_length=250, blank=True, null=True)
    diet = models.CharField(max_length=250, blank=True, null=True)
    behavior = models.CharField(max_length=250, blank=True, null=True)
    habitat_impact = models.CharField(max_length=250, blank=True, null=True)
    conservation_status = models.CharField(max_length=250, blank=True, null=True)
    conservation_measures = models.CharField(max_length=250, blank=True, null=True)
    reproduction = models.CharField(max_length=250, blank=True, null=True)
    gestation_period = models.CharField(max_length=250, blank=True, null=True)
    life_span = models.CharField(max_length=250, blank=True, null=True)
    predators = models.TextField(blank=True, null=True)
    prey = models.TextField(blank=True, null=True)
    ethical_medicinal_uses = models.TextField(blank=True, null=True)
    threats = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to=animal_media_upload_path, null=True, blank=True)
    video = models.FileField(upload_to=animal_media_upload_path, null=True, blank=True)
    audio = models.FileField(upload_to=animal_media_upload_path, null=True, blank=True)
    citation = models.TextField(blank=True, null=True) 
    contributor = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # ✅ Use AUTH_USER_MODEL instead of direct reference
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='animal_profile_contributions'
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    review_feedback = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.english_name} ({self.scientific_name})"

class AnimalLocalName(models.Model):
    animal_local_name_id = models.AutoField(primary_key=True)
    local_name = models.CharField(max_length=250, db_index=True)
    language = models.CharField(max_length=250, db_index=True)
    animal = models.ForeignKey(
        AnimalProfile,
        on_delete=models.CASCADE,
        related_name='local_names',
        null=True,
        help_text="The animal associated with this local name."
    )
    contributor = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # ✅ Use AUTH_USER_MODEL instead of direct reference
        on_delete=models.SET_NULL, 
        related_name='local_name_contributions',
        null=True,
        help_text="Contributor who added this local name."
    )

    class Meta:
        unique_together = ('animal', 'local_name', 'language')
        ordering = ['local_name']

    def __str__(self):
        return f"{self.local_name} ({self.language}) for {self.animal.english_name} ({self.animal.scientific_name})"

class AnimalImageGallery(models.Model):
    animal_english_name = models.CharField(max_length=250, db_index=True)
    image = models.ImageField(upload_to="animal_gallery/", blank=True, null=True)
    caption = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Image: {self.caption} ({self.animal_english_name})"

class AnimalVideoGallery(models.Model):
    animal_english_name = models.CharField(max_length=250, db_index=True)
    video = models.FileField(upload_to="animal_videos/", blank=True, null=True)
    caption = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Video: {self.caption} ({self.animal_english_name})"

# Entry counter to track the number of entries for each model
class AnimalEntryCounter(models.Model):
    model_name = models.CharField(max_length=100, unique=True)
    total_entries = models.PositiveIntegerField(default=0)

    def increment(self):
        self.total_entries = models.F('total_entries') + 1
        self.save(update_fields=['total_entries'])

    def decrement(self):
        if self.total_entries > 0:
            self.total_entries = models.F('total_entries') - 1
            self.save(update_fields=['total_entries'])

    class Meta:
        ordering = ['model_name']

    def __str__(self):
        return f"{self.model_name} Total Entries: {self.total_entries}"
