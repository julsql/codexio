from django.db import models

class BD(models.Model):
    class Meta:
        db_table = 'BD'

    isbn = models.BigIntegerField()
    album = models.TextField()
    number = models.TextField()
    series = models.TextField()
    writer = models.TextField()
    illustrator = models.TextField()
    colorist = models.TextField()
    publisher = models.TextField()
    publication_date = models.TextField()
    edition = models.TextField()
    number_of_pages = models.TextField()
    rating = models.TextField()
    purchase_price = models.TextField()
    year_of_purchase = models.TextField()
    place_of_purchase = models.TextField()
    deluxe_edition = models.TextField()
    signed_copy = models.TextField()
    ex_libris = models.TextField()
    synopsis = models.TextField()
    image = models.TextField()

    def __str__(self) -> str:
        return self.album
