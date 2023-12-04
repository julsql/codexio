from django.db import models


class BD(models.Model):
    class Meta:
        db_table = 'BD'

    isbn = models.BigIntegerField(primary_key=True)
    Album = models.TextField()
    Numéro = models.TextField()
    Série = models.TextField()
    Scénariste = models.TextField()
    Dessinateur = models.TextField()
    Couleur = models.TextField()
    Éditeur = models.TextField()
    Date_de_parution = models.TextField(db_column='Date de parution')
    Édition = models.TextField()
    Nombre_de_pages = models.TextField(db_column='Nombre de pages')
    Cote = models.TextField()
    Prix_d_achat = models.TextField(db_column="Prix d'achat")
    Année_d_achat = models.TextField(db_column="Année d'achat")
    Lieu_d_achat = models.TextField(db_column="Lieu d'achat")
    Dédicace = models.TextField()
    Ex_Libris = models.TextField(db_column='Ex Libris')
    Synopsis = models.TextField()
    Image = models.TextField()

    def __str__(self):
        return self.Album
