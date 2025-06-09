from django.conf import settings

from django.db import models


class Collection(models.Model):
    title = models.CharField(max_length=100)
    accounts = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="collections"
    )
    token = models.CharField(max_length=128, unique=True, editable=False)
    doc_name = models.CharField(max_length=100)
    sheet_name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.title
