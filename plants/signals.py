from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import PlantEntryCounter, Plant, PlantLocalName, MedicinalPlant, MedicinalPlant, MedicinalLocalPlantName, PlantImageGallery, PlantVideoGallery, PlantClassification, ScientificClassification

def update_entry_counter(model_name, increment=True):
    counter, _ = PlantEntryCounter.objects.get_or_create(model_name=model_name)
    if increment:
        counter.increment()
    else:
        counter.decrement()

@receiver(post_save, sender=Plant)
@receiver(post_save, sender=PlantLocalName)
@receiver(post_save, sender=MedicinalPlant)
@receiver(post_save, sender=MedicinalLocalPlantName)
@receiver(post_save, sender=ScientificClassification)
@receiver(post_save, sender=PlantImageGallery)
@receiver(post_save, sender=PlantVideoGallery)
@receiver(post_save, sender=PlantClassification)
def increment_entry_counter(sender, instance, created, **kwargs):
    if created:
        update_entry_counter(sender.__name__, increment=True)

@receiver(post_delete, sender=Plant)
@receiver(post_delete, sender=PlantLocalName)
@receiver(post_delete, sender=MedicinalPlant)
@receiver(post_delete, sender=MedicinalLocalPlantName)
@receiver(post_delete, sender=ScientificClassification)
@receiver(post_delete, sender=PlantImageGallery)
@receiver(post_delete, sender=PlantVideoGallery)
@receiver(post_delete, sender=PlantClassification)
def decrement_entry_counter(sender, instance, **kwargs):
    update_entry_counter(sender.__name__, increment=False)
