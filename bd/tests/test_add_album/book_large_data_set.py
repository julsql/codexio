from datetime import date

from main.core.domain.model.book import Book

BOVARY_ISBN = 9782070413119

# Données par source
BOVARY_DATA = {
    'BOOK': Book(isbn=9782070413119,
                 title='Madame Bovary',
                 writer='Gustave Flaubert, Thierry Laget',
                 translator='',
                 publisher='Gallimard Education',
                 collection_book='',
                 publication_date=date(2001, 1, 1),
                 edition='',
                 number_of_pages=532,
                 literary_genre='Fiction',
                 style='',
                 origin_language='fr',
                 synopsis="Fille d'un riche fermier, Emma Rouault épouse Charles Bovary, "
                          "officier de santé et veuf récent d'une femme tyrannique. Élevée "
                          'dans un couvent, Emma aspire à vivre dans le monde de rêve dont '
                          "parlent les romans à l'eau de rose qu'elle y a lu. Un bal au "
                          "château de Vaubyessard la persuade qu'un tel monde existe, mais "
                          "le décalage qu'elle découvre avec sa propre vie déclenche chez "
                          "elle une maladie nerveuse. La naissance d'une fille la distrait "
                          'un peu, mais bientôt Emma cède aux avances de Rodolphe. Elle '
                          "veut s'enfuir avec son amant qui, lâche, l'abandonne... [RERO]",
                 image='http://books.google.com/books/content?id=1ThlAAAAMAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api'),
}

BOVARY = BOVARY_DATA['BOOK']