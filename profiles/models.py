from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mail_activated = models.BooleanField(default=False)
    bio = models.CharField(max_length=256, default='')
    picture = models.ImageField(upload_to='profile_pictures', null=True)
    cover = models.ImageField(upload_to='profile_covers', null=True)


class settings(models.Model):

    LIGHT = 'li'
    DARK = 'da'
    WEBSITE_MODES = [
        (LIGHT, 'Light'),
        (DARK, 'Dark'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    delayed = models.BooleanField(default=True)
    mail_time = models.TimeField(auto_now_add=True)
    anonymous_posts = models.BooleanField(default=False)
    anonymous_comments = models.BooleanField(default=False)
    posts_comments = models.BooleanField(default=True)
    posts_messages = models.BooleanField(default=True)
    mode = models.CharField(max_length=2,
                            choices=WEBSITE_MODES,
                            default=LIGHT,
                            )