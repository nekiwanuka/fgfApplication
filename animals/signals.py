from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import AnimalProfile, AnimalClassification, AnimalLocalName, AnimalEntryCounter

# Signal Handlers to Automatically Update Counters
@receiver(post_save, sender=AnimalProfile)
@receiver(post_save, sender=AnimalClassification)
@receiver(post_save, sender=AnimalLocalName)
def increment_entry_counter(sender, instance, created, **kwargs):
    if created:
        counter, _ = AnimalEntryCounter.objects.get_or_create(model_name=sender.__name__)
        counter.increment()

@receiver(post_delete, sender=AnimalProfile)
@receiver(post_delete, sender=AnimalClassification)
@receiver(post_delete, sender=AnimalLocalName)
def decrement_entry_counter(sender, instance, **kwargs):
    counter, _ = AnimalEntryCounter.objects.get_or_create(model_name=sender.__name__)
    counter.decrement()