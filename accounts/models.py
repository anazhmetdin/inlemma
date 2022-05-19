from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from .utils import randomUsername, validUsername

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
            User.objects.filter(username=instance.username).update(username=username)
