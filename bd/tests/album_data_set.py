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
ASTERIX = {**ASTERIX_DATA['BDPHILE'], 'ISBN': str(ASTERIX_ISBN)}

ASTERIX_LIST_RESULT = [
    ASTERIX_ISBN, ASTERIX['Album'], ASTERIX['Numéro'], ASTERIX['Série'],
    ASTERIX['Scénario'], ASTERIX['Dessin'], ASTERIX['Couleurs'], ASTERIX['Éditeur'],
    ASTERIX['Date de publication'], ASTERIX['Édition'], ASTERIX['Pages'],
    None, ASTERIX['Prix'], None, '', False, '', ASTERIX['Synopsis'], ASTERIX['Image']
]

# Formats de liste
ASTERIX_LIST = [str(val) if isinstance(val, (int, float)) else val for val in [
    ASTERIX_ISBN, ASTERIX['Album'], ASTERIX['Numéro'], ASTERIX['Série'],
    ASTERIX['Scénario'], ASTERIX['Dessin'], ASTERIX['Couleurs'], ASTERIX['Éditeur'],
    ASTERIX['Date de publication'], ASTERIX['Édition'], ASTERIX['Pages'],
    '', ASTERIX['Prix'], '', '', '', '', '', '', ASTERIX['Synopsis'], ASTERIX['Image']
]]

# Format base de données
ALBUM_EXEMPLE = {
    "isbn": ASTERIX_ISBN,
    "album": ASTERIX['Album'],
    "number": ASTERIX['Numéro'],
    "series": ASTERIX['Série'],
    "writer": ASTERIX['Scénario'],
    "illustrator": ASTERIX['Dessin'],
    "colorist": ASTERIX['Couleurs'],
    "publisher": ASTERIX['Éditeur'],
    "publication_date": datetime.strptime(ASTERIX['Date de publication'], '%Y-%m-%d').date(),
    "edition": ASTERIX['Édition'],
    "number_of_pages": ASTERIX['Pages'],
    "rating": 10.0,
    "purchase_price": ASTERIX['Prix'],
    "year_of_purchase": 2025,
    "place_of_purchase": "Lyon",
    "deluxe_edition": False,
    "localisation": "",
    "synopsis": ASTERIX['Synopsis'],
    "image": ASTERIX['Image']
}

FIRST_LINE = [
    "ISBN", "Album", "Numéro", "Série", "Scénariste", "Dessinateur", "Couleur", "Éditeur", "Date de parution",
    "Édition", "Nombre de planches", "Cote", "Prix d'achat", "Année d'achat", "Lieu d'achat", "Tirage de tête",
    "Dédicace", "Ex Libris", "Emplacement", "Synopsis", "Image"]

FIRST_LINE_DATABASE = [
    'isbn', 'album', 'number', 'series', 'writer', 'illustrator', 'colorist', 'publisher',
    'publication_date', 'edition', 'number_of_pages', 'rating', 'purchase_price', 'year_of_purchase',
    'place_of_purchase', 'deluxe_edition', "localisation", 'synopsis', 'image']
