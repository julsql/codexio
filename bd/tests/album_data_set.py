from datetime import datetime

# ISBN et URLs
ASTERIX_ISBN = 9782864976165
ASTERIX_URLS = {
    'BDPHILE': "https://www.bdphile.fr/album/view/160391/",
    'BDGEST': "https://www.bedetheque.com/BD-Asterix-Hors-Serie-C14-L-Empire-du-Milieu-467639.html",
    'BDFUGUE': "https://www.bdfugue.com/catalogsearch/result/?q=9782864976165"
}

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

# Données par source
ASTERIX_DATA = {
    'BDPHILE': {
        'Album': "L'empire du milieu",
        'Série': "Astérix (Albums des films)",
        'Numéro': "10",
        'Scénario': "Olivier Gay",
        'Dessin': "Fabrice Tarrin",
        'Couleurs': "Thierry Mébarki",
        'Éditeur': "Albert René",
        'Date de publication': "2023-02-08",
        'Pages': 48,
        'Prix': 10.5,
        'Édition': "Édition originale Noté : Impression en décembre 2022 - n° 616-5-01 Impression et reliure par Pollina - n°13651",
        'Synopsis': "Nous sommes en 50 av J.-C. Loin, très loin du petit village d'Armorique que nous connaissons bien,"
                    " l'Impératrice de Chine est emprisonnée suite à coup d'état fomenté par l'infâme Deng Tsin Qin."
                    "<br/>La princesse Fu Yi, fille unique de l'Impératrice, aidée par sa fidèle guerrière Tat Han et"
                    " Graindemaïs, le neveu du marchand phénicien Epidemaïs, s'enfuit pour demander de l'aide aux"
                    " Irréductibles Gaulois.",
        'Image': "https://static.bdphile.fr/images/media/cover/0160/160391.jpg"
    },
    'BDGEST': {
        'Album': "L'Empire du Milieu",
        'Couleurs': "Thierry Mébarki",
        'Scénario': "Olivier Gay",
        "Série": "Astérix (Hors Série)",
        "Éditeur": "Les Éditions Albert René",
        'Dessin': "Fabrice Tarrin",
        'Date de publication': '2023-02-08',
        'Pages': 44,
        'Synopsis': "Nous sommes en 50 av J.-C. Loin, très loin du petit village "
                    "d'Armorique que nous connaissons bien, l'Impératrice de Chine "
                    "est emprisonnée suite à un coup d'état fomenté par l'infâme Deng "
                    "Tsin Qin. La princesse Fu Yi, fille unique de l'Impératrice, "
                    'aidée par sa fidèle guerrière Tat Han et Graindemaïs, le neveu '
                    "du marchand phénicien Épidemaïs, s'enfuit pour demander de "
                    "l'aide aux Irréductibles Gaulois.\n"
                    '\n'
                    'Une histoire originale basée sur le scénario du film Astérix & '
                    "Obélix, L'Empire du Milieu réalisé par Guillaume Canet.",
        'Image': "https://www.bedetheque.com/media/Couvertures/Couv_467639.jpg",
    },
    'BDFUGUE': {
        'Album': "L'empire du milieu (album illustré)",
        'Série': "Astérix",
        'Numéro': 1,
        'Scénario': "Olivier Gay",
        'Dessin': "Fabrice Tarrin",
        'Éditeur': "ALBERT RENE",
        'Date de publication': "2023-02-08",
        'Pages': 48,
        'Prix': 10.9,
        'Synopsis': 'NOUVEL ALBUM ILLUSTRÉ   Nous sommes en 50 av J.-C. Loin, très '
                    "loin du petit village d'Armorique que nous connaissons bien, "
                    "l'Impératrice de Chine est emprisonnée suite à coup d'état "
                    "fomenté par l'infâme Deng Tsin Qin.  \r\n"
                    '\r\n'
                    "La princesse Fu Yi, fille unique de l'Impératrice, aidée par sa "
                    'fidèle guerrière Tat Han et Graindemaïs, le neveu du marchand '
                    "phénicien Epidemaïs, s'enfuit pour demander de l'aide aux "
                    'Irréductibles Gaulois.\r\n'
                    '\r\n'
                    'Une histoire originale basée sur le scénario du film Astérix & '
                    "Obélix, L'Empire du Milieu réalisé par Guillaume Canet.",
        'Image': "https://www.bdfugue.com/media/catalog/product/cache/0d950bd4d3aaddc02a824ea154d9c41e/9/7/9782864976165_1_75.jpg",
    }
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
