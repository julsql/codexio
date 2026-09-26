from django.db import models
from django.db.models import Manager


class AlbumInfosCache(models.Model):
    """Notice renvoyée par une source externe pour un ISBN, mémorisée pour éviter de la redemander"""
    objects: Manager

    source = models.CharField(max_length=100)
    isbn = models.BigIntegerField()
    payload = models.JSONField()
    fetched_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            # Crée aussi l'index qui sert les lectures du cache
            models.UniqueConstraint(fields=["source", "isbn"], name="unique_album_cache_source_isbn"),
        ]

    def __str__(self) -> str:
        return f"{self.source} / {self.isbn}"
