ASTERIX_ISBN = 9782864976165
ASTERIX_BDPHILE_LINK = "https://www.bdphile.fr/album/view/160391/"
ASTERIX_BDFUGUE_LINK = "https://www.bdfugue.com/catalogsearch/result/?q=9782864976165"
album = "L'empire du milieu"
couleurs = "Thierry Mébarki"
date_de_publication = "2023-02-08"
dessin = "Fabrice Tarrin"
image = "https://static.bdphile.fr/images/media/cover/0160/160391.jpg"
numero = "10"
pages = 48
prix = 10.5
scenario = "Olivier Gay"
synopsis = ("Nous sommes en 50 av J.-C. Loin, très loin du petit village d'Armorique que nous connaissons bien,"
            " l'Impératrice de Chine est emprisonnée suite à coup d'état fomenté par l'infâme Deng Tsin Qin."
            "<br/>La princesse Fu Yi, fille unique de l'Impératrice, aidée par sa fidèle guerrière Tat Han et"
            " Graindemaïs, le neveu du marchand phénicien Epidemaïs, s'enfuit pour demander de l'aide aux"
            " Irréductibles Gaulois.")
serie = "Astérix (Albums des films)"
editeur = "Albert René"
edition = "Édition originale Noté : Impression en décembre 2022 - n° 616-5-01 Impression et reliure par Pollina - n°13651"

FIRST_LINE = [
    "ISBN", "Album", "Numéro", "Série", "Scénariste", "Dessinateur", "Couleur", "Éditeur", "Date de parution",
    "Édition", "Nombre de pages", "Cote", "Prix d'achat", "Année d'achat", "Lieu d'achat", "Tirage de tête",
    "Dédicace", "Ex Libris", "Synopsis", "Image"]

ASTERIX_WEB = {
    'Album': album,
    'Couleurs': couleurs,
    'Date de publication': date_de_publication,
    'Dessin': dessin,
    'Image':  image,
    'Numéro': numero,
    'Pages': pages,
    'Prix': prix,
    'Scénario': scenario,
    'Synopsis': synopsis,
    'Série': serie,
    'Éditeur': editeur,
    'Édition': edition,
}

ASTERIX = ASTERIX_WEB.copy()
ASTERIX['ISBN'] = ASTERIX_ISBN


ASTERIX_LIST = [
    ASTERIX_ISBN,
    album,
    numero,
    serie,
    scenario,
    dessin,
    couleurs,
    editeur,
    date_de_publication,
    edition,
    pages,
    '',
    prix,
    '',
    '',
    '',
    '',
    '',
    synopsis,
    image
]