from django.db import models
from django.db.models import Manager


class BD(models.Model):
    class Meta:
        db_table = 'BD'

    objects: Manager

    isbn = models.BigIntegerField()
    album = models.TextField()
    number = models.TextField()
    series = models.TextField()
    writer = models.TextField()
    illustrator = models.TextField()
    colorist = models.TextField()
    publisher = models.TextField()
    publication_date = models.DateField(null=True)
    edition = models.TextField()
    number_of_pages = models.IntegerField(null=True)
    rating = models.FloatField(null=True)
    purchase_price = models.FloatField(null=True)
    year_of_purchase = models.IntegerField(null=True)
    place_of_purchase = models.TextField()
    deluxe_edition = models.BooleanField()
    localisation = models.TextField()
    synopsis = models.TextField()
    image = models.TextField()

    def __str__(self) -> str:
        return self.album
