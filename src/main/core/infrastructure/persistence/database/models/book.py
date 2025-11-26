from django.db import models
from django.db.models import Manager

from main.core.infrastructure.persistence.database.models.collection import Collection


class Book(models.Model):
    objects: Manager

    isbn = models.BigIntegerField()
    title = models.TextField()
    writer = models.CharField(max_length=50)
    translator = models.TextField()
    publisher = models.TextField()
    collection_book = models.TextField()
    publication_date = models.DateField(null=True)
    edition = models.TextField()
    number_of_pages = models.IntegerField(null=True)
    literary_genre = models.TextField()
    style = models.TextField()
    origin_language = models.TextField()
    purchase_price = models.FloatField(null=True)
    year_of_purchase = models.IntegerField(null=True)
    place_of_purchase = models.TextField()
    localisation = models.TextField()
    synopsis = models.TextField()
    image = models.URLField()
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='book_rows')

    def __str__(self) -> str:
        return self.title
