from django.db import models
from django.db.models import Manager


class BD(models.Model):
    class Meta:
        db_table = 'BD'

    objects: Manager

    isbn = models.BigIntegerField()
    album = models.CharField(max_length=255)
    number = models.CharField(max_length=50)
    series = models.CharField(max_length=255)
    writer = models.CharField(max_length=255)
    illustrator = models.CharField(max_length=255)
    colorist = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    publication_date = models.DateField(null=True)
    edition = models.CharField(max_length=100)
    number_of_pages = models.IntegerField(null=True)
    rating = models.FloatField(null=True)
    purchase_price = models.FloatField(null=True)
    year_of_purchase = models.IntegerField(null=True)
    place_of_purchase = models.TextField()
    deluxe_edition = models.BooleanField(default=False)
    localisation = models.TextField()
    synopsis = models.TextField()
    image = models.URLField()

    def __str__(self) -> str:
        return self.album
