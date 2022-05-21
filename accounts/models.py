from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from .utils import randomUsername, validUsername


class User(AbstractUser):
    mail_activated = models.BooleanField(default=False)

@receiver(models.signals.post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    if created:
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
