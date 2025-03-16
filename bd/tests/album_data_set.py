ASTERIX_ISBN = 9782864976165
ASTERIX_BDPHILE_LINK = "https://www.bdphile.fr/album/view/160391/"
ASTERIX_BDGEST_LINK = "https://www.bedetheque.com/BD-Asterix-Hors-Serie-C14-L-Empire-du-Milieu-467639.html"
ASTERIX_BDFUGUE_LINK = "https://www.bdfugue.com/catalogsearch/result/?q=9782864976165"
album_phile = "L'empire du milieu"
couleurs_phile = "Thierry Mébarki"
date_de_publication_phile = "2023-02-08"
dessin_phile = "Fabrice Tarrin"
image_phile = "https://static.bdphile.fr/images/media/cover/0160/160391.jpg"
numero_phile = "10"
pages_phile = 48
prix_phile = 10.5
scenario_phile = "Olivier Gay"
synopsis_phile = ("Nous sommes en 50 av J.-C. Loin, très loin du petit village d'Armorique que nous connaissons bien,"
            " l'Impératrice de Chine est emprisonnée suite à coup d'état fomenté par l'infâme Deng Tsin Qin."
            "<br/>La princesse Fu Yi, fille unique de l'Impératrice, aidée par sa fidèle guerrière Tat Han et"
            " Graindemaïs, le neveu du marchand phénicien Epidemaïs, s'enfuit pour demander de l'aide aux"
            " Irréductibles Gaulois.")
serie_phile = "Astérix (Albums des films)"
editeur_phile = "Albert René"
edition_phile = "Édition originale Noté : Impression en décembre 2022 - n° 616-5-01 Impression et reliure par Pollina - n°13651"

album_gest = "L'Empire du Milieu"
couleurs_gest = "Thierry Mébarki"
date_de_publication_gest = "2023-02-08"
dessin_gest = "Fabrice Tarrin"
image_gest = "https://www.bedetheque.com/media/Couvertures/Couv_467639.jpg"
pages_gest = 44
scenario_gest = "Olivier Gay"
synopsis_gest = ("Nous sommes en 50 av J.-C. Loin, très loin du petit village "
                 "d'Armorique que nous connaissons bien, l'Impératrice de Chine "
                 "est emprisonnée suite à un coup d'état fomenté par l'infâme Deng "
                 "Tsin Qin. La princesse Fu Yi, fille unique de l'Impératrice, "
                 'aidée par sa fidèle guerrière Tat Han et Graindemaïs, le neveu '
                 "du marchand phénicien Épidemaïs, s'enfuit pour demander de "
                 "l'aide aux Irréductibles Gaulois.\n"
                 '\n'
                 'Une histoire originale basée sur le scénario du film Astérix & '
                 "Obélix, L'Empire du Milieu réalisé par Guillaume Canet.")
serie_gest = "Astérix (Hors Série)"
editeur_gest = "Les Éditions Albert René"


FIRST_LINE = [
    "ISBN", "Album", "Numéro", "Série", "Scénariste", "Dessinateur", "Couleur", "Éditeur", "Date de parution",
    "Édition", "Nombre de planches", "Cote", "Prix d'achat", "Année d'achat", "Lieu d'achat", "Tirage de tête",
    "Dédicace", "Ex Libris", "Synopsis", "Image"]

FIRST_LINE_DATABASE =[
    'isbn', 'album', 'number', 'series', 'writer', 'illustrator', 'colorist', 'publisher',
    'publication_date', 'edition', 'number_of_pages', 'rating', 'purchase_price', 'year_of_purchase',
    'place_of_purchase', 'deluxe_edition', 'synopsis', 'image']

ASTERIX_WEB_PHILE = {
    'Album': album_phile,
    'Couleurs': couleurs_phile,
    'Date de publication': date_de_publication_phile,
    'Dessin': dessin_phile,
    'Image':  image_phile,
    'Numéro': numero_phile,
    'Pages': pages_phile,
    'Prix': prix_phile,
    'Scénario': scenario_phile,
    'Synopsis': synopsis_phile,
    'Série': serie_phile,
    'Éditeur': editeur_phile,
    'Édition': edition_phile,
}

ASTERIX_WEB_GEST = {
    'Album': album_gest,
    'Couleurs': couleurs_gest,
    'Date de publication': date_de_publication_gest,
    'Dessin': dessin_gest,
    'Image':  image_gest,
    'Pages': pages_gest,
    'Scénario': scenario_gest,
    'Synopsis': synopsis_gest,
    'Série': serie_gest,
    'Éditeur': editeur_gest,
}

ASTERIX = ASTERIX_WEB_PHILE.copy()
ASTERIX['ISBN'] = ASTERIX_ISBN

ASTERIX_LIST = [
    ASTERIX_ISBN,
    album_phile,
    numero_phile,
    serie_phile,
    scenario_phile,
    dessin_phile,
    couleurs_phile,
    editeur_phile,
    date_de_publication_phile,
    edition_phile,
    pages_phile,
    '',
    str(prix_phile),
    '',
    '',
    '',
    '',
    '',
    synopsis_phile,
    image_phile
]

ASTERIX_LIST_2 = [
    ASTERIX_ISBN,
    album_phile,
    numero_phile,
    serie_phile,
    scenario_phile,
    dessin_phile,
    couleurs_phile,
    editeur_phile,
    date_de_publication_phile,
    edition_phile,
    pages_phile,
    '',
    prix_phile,
    '',
    '',
    '',
    '',
    '',
    synopsis_phile,
    image_phile
]

ASTERIX_LIST_RESULT = [
    ASTERIX_ISBN,
    album_phile,
    numero_phile,
    serie_phile,
    scenario_phile,
    dessin_phile,
    couleurs_phile,
    editeur_phile,
    date_de_publication_phile,
    edition_phile,
    pages_phile,
    None,
    prix_phile,
    None,
    '',
    False,
    synopsis_phile,
    image_phile
]

ASTERIX_LIST_STR = [
    str(ASTERIX_ISBN),
    album_phile,
    numero_phile,
    serie_phile,
    scenario_phile,
    dessin_phile,
    couleurs_phile,
    editeur_phile,
    date_de_publication_phile,
    edition_phile,
    str(pages_phile),
    '',
    str(prix_phile).replace('.', ','),
    '',
    '',
    '',
    '',
    '',
    synopsis_phile,
    image_phile
]