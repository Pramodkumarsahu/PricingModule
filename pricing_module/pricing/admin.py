from django.contrib import admin
from pricing import models
# Register your models here.

@admin.register(models.PricingConfig)
class PricingConfigAdmin(admin.ModelAdmin):
    list_display = ('name', 'active', 'created_at')
    search_fields = ('name',)
    list_filter = ('active',)
    ordering = ('-created_at',)


class TimeMultiplierTierAdmin(admin.ModelAdmin):
    list_display = ('pricing_config', 'from_minute', 'to_minute', 'multiplier')
    search_fields = ('pricing_config__name',)
    list_filter = ('pricing_config',)
    ordering = ('pricing_config', 'from_minute')

admin.site.register(models.TimeMultiplierTier)

class ConfigLogAdmin(admin.ModelAdmin):
    list_display = ('config', 'actor', 'action', 'timestamp')
    search_fields = ('config__name', 'actor__username', 'action')
    ordering = ('timestamp',)
admin.site.register(models.ConfigLog, ConfigLogAdmin)