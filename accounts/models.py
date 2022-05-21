from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.forms import ValidationError
from .utils import randomUsername, validUsername, validEmail


class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mail_activated = models.BooleanField(default=False)

@receiver(models.signals.post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    if created:
        profile.objects.create(user=instance)
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