from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class PricingConfig(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    days_applicable = models.JSONField(help_text="List of days like ['Mon', 'Tue']")

    distance_base_price = models.FloatField()
    distance_base_km = models.FloatField()
    distance_additional_price = models.FloatField()

    waiting_charge = models.FloatField(help_text="Per 3 mins")
    free_waiting_minutes = models.IntegerField(default=3)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class TimeMultiplierTier(models.Model):
    pricing_config = models.ForeignKey(PricingConfig, on_delete=models.CASCADE, related_name="time_multipliers")
    from_minute = models.IntegerField()
    to_minute = models.IntegerField()
    multiplier = models.FloatField()

    class Meta:
        ordering = ['from_minute']

    def __str__(self):
        return self.pricing_config.name + f" ({self.from_minute}-{self.to_minute} mins) x {self.multiplier}"


class ConfigLog(models.Model):
    config = models.ForeignKey(PricingConfig, on_delete=models.CASCADE)
    actor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    @receiver(post_save, sender=PricingConfig)
    def log_config_change(sender, instance, created, **kwargs):
        print("##########3 Config change detected:", instance.name,instance.user, "Created:", created)
        if created:
            ConfigLog.objects.create(config=instance, actor=instance.user, action="Created")
        else:
            ConfigLog.objects.create(config=instance, actor=instance.user, action="Updated")

    def __str__(self):
        return f"{self.actor.username if self.actor else 'Admin'}"