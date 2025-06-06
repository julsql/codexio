from django.db import models
from django.db.models import Manager

from main.models import AppUser


class Collection(models.Model):
    objects: Manager

    title = models.CharField(max_length=100)
    accounts = models.ManyToManyField(AppUser, related_name="collections")

    def __str__(self) -> str:
        return self.title
