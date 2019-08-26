from django.db import models

# Create your models here.

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender = settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance = None, created = False, **kwargs):
    if created:
        Token.objects.create(user = instance)

class UserStatus(models.Model):
    username = models.CharField(unique = True, max_length = 200)
    timestamp = models.DateTimeField(null = True, auto_now_add = True)
    status = models.CharField(null = True, max_length = 200)
    class Meta:
        ordering = ['timestamp']

class GPSCoordinates(models.Model):
    userstatus_gps = models.ForeignKey(UserStatus, null=True, related_name='userstatus_gps', on_delete=models.CASCADE)
    longitude = models.FloatField(default=0.0)
    latitude = models.FloatField(default=0.0)
    altitude = models.FloatField(default=0.0)
    timestamp = models.DateTimeField(null = False, auto_now_add = True)
    class Meta:
        get_latest_by = "timestamp"
     # This table contains whom being followd by user and who are following