from datetime import datetime

from tests.test_add_album.album_large_data_set import ASTERIX_ISBN, ASTERIX_DATA

# Structures de données communes
COLUMN_HEADERS = {
    'SHEET': [
        "ISBN", "Album", "Numéro", "Série", "Scénariste", "Dessinateur", "Couleur",
        "Éditeur", "Date de parution", "Édition", "Nombre de planches", "Cote",
        "Prix d'achat", "Année d'achat", "Lieu d'achat", "Tirage de tête",
        "Dédicace", "Ex Libris", "Emplacement", "Synopsis", "Image"
    ],
    'DATABASE': [
        'isbn', 'album', 'number', 'series', 'writer', 'illustrator', 'colorist',
        'publisher', 'publication_date', 'edition', 'number_of_pages', 'rating',
        'purchase_price', 'year_of_purchase', 'place_of_purchase', 'deluxe_edition',
        "localisation", 'synopsis', 'image'
    ]
}

# Données consolidées
ASTERIX = ASTERIX_DATA['BDPHILE']

ASTERIX_LIST_RESULT = [
    ASTERIX_ISBN, ASTERIX.titre, ASTERIX.numero, ASTERIX.serie,
    ASTERIX.scenariste, ASTERIX.dessinateur, ASTERIX.coloriste, ASTERIX.editeur,
    ASTERIX.date_publication, ASTERIX.edition, ASTERIX.nombre_pages,
    None, ASTERIX.prix, None, '', False, '', ASTERIX.synopsis, ASTERIX.image_url
]

# Formats de liste
ASTERIX_LIST = [str(val) if isinstance(val, (int, float)) else val for val in [
    ASTERIX.isbn,
    ASTERIX.titre,
    ASTERIX.numero,
    ASTERIX.serie,
    ASTERIX.scenariste,
    ASTERIX.dessinateur,
    ASTERIX.coloriste,
    ASTERIX.editeur,
    ASTERIX.date_publication.strftime("%Y-%m-%d") if ASTERIX.date_publication else "",
    ASTERIX.edition,
    ASTERIX.nombre_pages,
    "",
    float(ASTERIX.prix) if ASTERIX.prix else "",
    "",
    "",
    "",
    "",
    "",
    "",
    ASTERIX.synopsis,
    ASTERIX.image_url

]]

# Format base de données
ALBUM_EXEMPLE = {
    "isbn": ASTERIX.isbn,
    "album": ASTERIX.titre,
    "number": ASTERIX.numero,
    "series": ASTERIX.serie,
    "writer": ASTERIX.scenariste,
    "illustrator": ASTERIX.dessinateur,
    "colorist": ASTERIX.coloriste,
    "publisher": ASTERIX.editeur,
    "publication_date": ASTERIX.date_publication,
    "edition": ASTERIX.edition,
    "number_of_pages": ASTERIX.nombre_pages,
    "rating": 10.0,
    "purchase_price": ASTERIX.prix,
    "year_of_purchase": 2025,
    "place_of_purchase": "Lyon",
    "deluxe_edition": False,
    "localisation": "",
    "synopsis": ASTERIX.synopsis,
    "image": ASTERIX.image_url
}

FIRST_LINE = [
    "ISBN", "Album", "Numéro", "Série", "Scénariste", "Dessinateur", "Couleur", "Éditeur", "Date de parution",
    "Édition", "Nombre de planches", "Cote", "Prix d'achat", "Année d'achat", "Lieu d'achat", "Tirage de tête",
    "Dédicace", "Ex Libris", "Emplacement", "Synopsis", "Image"]

FIRST_LINE_DATABASE = [
    'isbn', 'album', 'number', 'series', 'writer', 'illustrator', 'colorist', 'publisher',
    'publication_date', 'edition', 'number_of_pages', 'rating', 'purchase_price', 'year_of_purchase',
    'place_of_purchase', 'deluxe_edition', "localisation", 'synopsis', 'image']
