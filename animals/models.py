from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import FgfUser


class AnimalClassification(models.Model):
    animal_classification_id = models.AutoField(primary_key=True)
    kingdom_name = models.CharField(max_length=250)
    species = models.CharField(max_length=250)
    number_of_species = models.IntegerField(default=1, null=True)
    animal_class = models.CharField(max_length=250)
    order = models.CharField(max_length=250)
    domestic = models.BooleanField(default=False)
    wild_animal = models.BooleanField(default=False)
    contributors = models.ManyToManyField(FgfUser, blank=True, related_name='contributed_animal_classifications')

    def __str__(self):
        return f"{self.animal_class} ({self.kingdom_name})"


class AnimalProfile(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('published', 'Published'),
        ('rejected', 'Rejected'),
    ]

    animal_id = models.BigAutoField(primary_key=True)
    english_name = models.CharField(max_length=250)
    scientific_name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    areas_in_Uganda = models.CharField(max_length=250, blank=True, null=True)
    animal_classifications = models.ForeignKey(
        AnimalClassification, on_delete=models.SET_NULL, null=True, related_name='animals'
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
    image = models.ImageField(upload_to="animal_images", null=True, blank=True)
    video = models.FileField(upload_to="animal_videos", null=True, blank=True)
    audio = models.FileField(upload_to="animal_audios", null=True, blank=True)
    citation = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    review_feedback = models.TextField(blank=True, null=True)
    date_entered = models.DateTimeField(auto_now_add=True)
    contributors = models.ManyToManyField(FgfUser, blank=True, related_name='contributed_animals')


    def __str__(self):
        return f"{self.english_name} ({self.scientific_name})"


class AnimalLocalName(models.Model):
    animal_local_name_id = models.AutoField(primary_key=True)
    local_name = models.CharField(max_length=250)
    language = models.CharField(max_length=250)
    animal = models.ForeignKey(
        AnimalProfile,
        on_delete=models.CASCADE,
        related_name='local_names',
        null=True,
        help_text="The animal associated with this local name."
    )
    contributor = models.ForeignKey(
        FgfUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='local_name_contributions',
        help_text="Contributor who added this local name."
    )

    class Meta:
        unique_together = ('animal', 'local_name', 'language')  # Avoid duplicate local names for an animal in a language

    def __str__(self):
        return f"{self.local_name} ({self.language}) for {self.animal.english_name} ({self.animal.scientific_name})"



class AnimalEntryCounter(models.Model):
    total_entries = models.PositiveIntegerField(default=0)

    def increment(self):
        self.total_entries += 1
        self.save()

    def decrement(self):
        if self.total_entries > 0:
            self.total_entries -= 1
            self.save()

    def __str__(self):
        return f"Total Entries: {self.total_entries}"


# Signal Handlers to Automatically Increment Counter on Save
@receiver(post_save, sender=AnimalProfile)
@receiver(post_save, sender=AnimalClassification)
@receiver(post_save, sender=AnimalLocalName)
def increment_animal_entry_counter(sender, instance, created, **kwargs):
    if created:
        counter, _ = AnimalEntryCounter.objects.get_or_create(id=1)
        counter.increment()
