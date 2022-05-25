from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from profiles.models import profile, settings
from .utils import randomUsername, validUsername

User._meta.get_field('email')._unique = True

@receiver(models.signals.post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    if created:
        profile.objects.create(user=instance)
        settings.objects.create(user=instance)
        username = instance.username
        notValid = True
        while notValid:
            try:
                validUsername(username, created)
                notValid = False
            except Exception as e:
                username = randomUsername()

        if username != instance.username:
            instance.username=username
            instance.save()

@receiver(models.signals.post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()