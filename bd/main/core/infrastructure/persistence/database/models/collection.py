from django.conf import settings
from django.db import models

from main.core.infrastructure.persistence.database.models.profile import Profile


class Collection(models.Model):
    title = models.CharField(max_length=100)
    token = models.CharField(max_length=128, unique=True, editable=False)
    doc_name = models.CharField(max_length=100)
    sheet_name = models.CharField(max_length=100)
    accounts = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="collections"
    )
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="collections")

    def __str__(self) -> str:
        return self.title
