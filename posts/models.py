from django.db import models
from django.contrib.auth.models import User


class post(models.Model):

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, db_index=True)
    title = models.CharField(max_length=128, blank=True, null=True)
    body = models.TextField(blank=False, null=False)
    anonymous = models.BooleanField()
    comments = models.BooleanField()
    messages = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)
    published_at = models.DateTimeField(auto_now_add=True)
    HTML = models.BooleanField(default=False)
    edited = models.BooleanField(default=False)


class comment(models.Model):

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, db_index=True)
    post = models.ForeignKey(to=post, on_delete=models.CASCADE, db_index=True)
    body = models.TextField(blank=False, null=False)
    anonymous = models.BooleanField()
    edited = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)