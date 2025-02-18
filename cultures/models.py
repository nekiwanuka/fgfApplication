from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from accounts.models import FgfUser  # Import the FgfUser model
from fgfplatform.constants import STATUS_CHOICES  # Import submission statuses

class ClanCount(models.Model):
    total_clans = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

class EthnicGroup(models.Model):
    ethnic_group_id = models.BigAutoField(primary_key=True)
    ethnic_group_name = models.CharField(max_length=250, unique=True)
    region_in_Uganda = models.CharField(max_length=250, blank=True, null=True)
    number_of_ethnicities = models.IntegerField(default=1, blank=True, null=True)
    number_of_languages = models.IntegerField(default=1, null=True)
    number_of_kingdoms_or_chiefdoms = models.IntegerField(default=1, null=True)
    citation = models.CharField(max_length=250, blank=True, null=True)
    contributor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="ethnic_groups")
    primary_contributor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="main_ethnic_groups")
    date_entered = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    review_feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.ethnic_group_name

class Ethnicity(models.Model):
    ethnicity_id = models.BigAutoField(primary_key=True)
    ethnicity_name = models.CharField(max_length=250, unique=True)
    region_in_Uganda = models.CharField(max_length=250, blank=True, null=True)
    language = models.CharField(max_length=250, blank=True, null=True)
    common_food_types = models.TextField(blank=True, null=True)
    staple_food = models.CharField(max_length=250, blank=True, null=True)
    main_cash_crop = models.CharField(max_length=250, blank=True, null=True)
    leisure_activities = models.TextField(blank=True, null=True)
    entertainment_activities = models.TextField(blank=True, null=True)
    denominations = models.TextField(blank=True, null=True)
    universal_rituals = models.TextField(blank=True, null=True)
    ceremonies = models.TextField(blank=True, null=True)
    citation = models.TextField(blank=True, null=True)
    contributor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="ethnicities")
    primary_contributor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="main_ethnicities")
    date_entered = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    review_feedback = models.TextField(blank=True, null=True)
    ethnic_group = models.ForeignKey(EthnicGroup, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.ethnicity_name

class CulturalKingdom(models.Model):
    LEADER_CHOICES = [
        ('king', _('King')),
        ('chief', _('Chief')),
    ]
    cultural_kingdom_id = models.BigAutoField(primary_key=True)
    kingdom_name = models.CharField(max_length=250, unique=True)
    title_of_leader = models.CharField(max_length=250, blank=True, null=True, choices=LEADER_CHOICES)
    number_of_clans = models.IntegerField(default=1, null=True)
    leader_name = models.CharField(max_length=250, blank=True, null=True)
    citation = models.CharField(max_length=250, blank=True, null=True)
    contributor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="cultural_kingdoms")
    primary_contributor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="main_cultural_kingdoms")
    date_entered = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    review_feedback = models.TextField(blank=True, null=True)
    ethnicity = models.ForeignKey(Ethnicity, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.kingdom_name

class Clan(models.Model):
    clan_id = models.BigAutoField(primary_key=True)
    clan_name = models.CharField(max_length=250, unique=True)
    clan_seat = models.CharField(max_length=250, blank=True)
    clan_anthem = models.TextField(blank=True, null=True)
    clan_roles = models.TextField(blank=True, null=True)
    totem = models.CharField(max_length=250, blank=True)
    secondary_totem = models.CharField(max_length=250, blank=True)
    clan_history = models.TextField(blank=True)
    clan_leader_title = models.CharField(max_length=250, blank=True)
    clan_leader_name = models.CharField(max_length=250, blank=True)
    cultural_sites = models.TextField(blank=True)
    male_names = models.TextField(blank=True)
    female_names = models.TextField(blank=True)
    reserved_male_names = models.TextField(blank=True)
    reserved_female_names = models.TextField(blank=True)
    taboos = models.TextField(blank=True)
    lead_god = models.CharField(max_length=250, blank=True)
    other_gods = models.CharField(max_length=250, blank=True)
    citation = models.TextField(blank=True, null=True)
    contributor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="clans")
    primary_contributor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="main_clans")
    date_entered = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    review_feedback = models.TextField(blank=True, null=True)
    ethnicity = models.ForeignKey(Ethnicity, on_delete=models.SET_NULL, null=True, blank=True)
    cultural_kingdom = models.ForeignKey(CulturalKingdom, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.clan_name

class ClanProfile(models.Model):
    ethnic_group = models.ForeignKey(EthnicGroup, on_delete=models.CASCADE)
    cultural_kingdom = models.ForeignKey(CulturalKingdom, on_delete=models.CASCADE)
    clan = models.ForeignKey(Clan, on_delete=models.CASCADE)
    editor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    citation = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    review_feedback = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(blank=True, null=True)

@receiver(post_save, sender=Clan)
@receiver(post_delete, sender=Clan)
def update_clan_count(sender, **kwargs):
    total = Clan.objects.count()
    ClanCount.objects.update_or_create(id=1, defaults={'total_clans': total})
