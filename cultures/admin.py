from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import EthnicGroup, Ethnicity, CulturalKingdom, Clan, ClanProfile, ClanCount

@admin.register(EthnicGroup)
class EthnicGroupAdmin(admin.ModelAdmin):
    list_display = ("ethnic_group_name", "region_in_Uganda", "status", "date_entered")
    search_fields = ("ethnic_group_name", "region_in_Uganda")
    list_filter = ("status", "region_in_Uganda")
    readonly_fields = ("date_entered",)

@admin.register(Ethnicity)
class EthnicityAdmin(admin.ModelAdmin):
    list_display = ("ethnicity_name", "region_in_Uganda", "status", "date_entered")
    search_fields = ("ethnicity_name", "region_in_Uganda")
    list_filter = ("status", "region_in_Uganda")
    readonly_fields = ("date_entered",)

@admin.register(CulturalKingdom)
class CulturalKingdomAdmin(admin.ModelAdmin):
    list_display = ("kingdom_name", "title_of_leader", "leader_name", "status", "date_entered")
    search_fields = ("kingdom_name", "leader_name")
    list_filter = ("status", "title_of_leader")
    readonly_fields = ("date_entered",)

@admin.register(Clan)
class ClanAdmin(admin.ModelAdmin):
    list_display = ("clan_name", "totem", "clan_leader_name", "status", "date_entered")
    search_fields = ("clan_name", "clan_leader_name", "totem")
    list_filter = ("status", "clan_leader_title")
    readonly_fields = ("date_entered",)

@admin.register(ClanProfile)
class ClanProfileAdmin(admin.ModelAdmin):
    list_display = ("clan", "cultural_kingdom", "ethnic_group", "editor", "status", "published_date")
    search_fields = ("clan__clan_name", "cultural_kingdom__kingdom_name", "ethnic_group__ethnic_group_name", "editor__email")
    list_filter = ("status", "editor")
    readonly_fields = ("date_created", "updated_at", "published_date")

@admin.register(ClanCount)
class ClanCountAdmin(admin.ModelAdmin):
    list_display = ("total_clans", "updated_at")
    readonly_fields = ("updated_at",)
