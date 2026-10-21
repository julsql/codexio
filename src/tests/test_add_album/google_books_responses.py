"""Réponses Google Books enregistrées, pour tester les adapters sans appel réseau.

Le contenu de l'API évolue (fiches retirées, `totalItems: 0`, 503 intermittents) :
les tests unitaires s'appuient sur ces payloads figés.
"""
from unittest.mock import MagicMock

from tests.test_add_album.album_large_data_set import ASTERIX_ISBN, SAMBRE_ISBN, THORGAL_ISBN, SAULE_ISBN
from tests.test_add_album.book_large_data_set import BOVARY_ISBN


def _isbn_identifiers(isbn: int) -> list[dict]:
    isbn_13 = str(isbn)
    return [
        {"type": "ISBN_10", "identifier": isbn_13[3:]},
        {"type": "ISBN_13", "identifier": isbn_13},
    ]


def _cover(volume_id: str) -> dict:
    url = f"http://books.google.com/books/content?id={volume_id}&printsec=frontcover&img=1&zoom=1&source=gbs_api"
    return {"smallThumbnail": url.replace("zoom=1", "zoom=5"), "thumbnail": url}


def _volumes(*items: dict) -> dict:
    return {"kind": "books#volumes", "totalItems": len(items), "items": list(items)}


GOOGLE_BOOKS_RESPONSES = {
    ASTERIX_ISBN: _volumes({
        "id": "evqxzwEACAAJ",
        "volumeInfo": {
            "title": "L'empire du milieu",
            "authors": ["Olivier*Tarrin Gay (Fabrice)"],
            "publishedDate": "2023",
            "description": "Suite à un coup d&#39;Etat qui a renversé l&#39;impératrice, la princesse chinoise "
                           "Fu Yi part demander de l&#39;aide aux irréductibles Gaulois. [electre]",
            "industryIdentifiers": _isbn_identifiers(ASTERIX_ISBN),
            "imageLinks": _cover("evqxzwEACAAJ"),
            "language": "fr",
        },
    }),
    SAMBRE_ISBN: _volumes({
        "id": "sAmBrE3AAAAJ",
        "volumeInfo": {
            "title": "Hugo & Iris",
            "subtitle": "Tome 3, Hiver 1831, La lune qui regarde",
            "authors": ["Yslaire"],
            "publishedDate": "2009-11-25",
            "pageCount": 58,
            "description": "La guerre des Sambre est une collection de romans d'amour, "
                           "dont la série principale, Sambre, conte l'histoire de Bernard "
                           "et Julie... Elle se poursuit aujourd'hui avec celle de leurs "
                           "parents, Hugo & Iris. L'histoire de chaque génération se "
                           'décline en trois ou quatre albums et peut se lire séparément, '
                           "comme une oeuvre exeptionnelle, ou comme un cycle d'une folie "
                           'amoureuse qui traverse les générations...',
            "industryIdentifiers": _isbn_identifiers(SAMBRE_ISBN),
            "language": "fr",
        },
    }),
    THORGAL_ISBN: _volumes({
        "id": "tHoRgAl1AAAJ",
        "volumeInfo": {
            "title": "La magicienne trahie ; suivi de Presque le paradis...",
            "authors": ["Jean van Hamme", "Grzegorz Rosinski"],
            "publisher": "Les Editions du Lombard",
            "publishedDate": "2000-08-24",
            "pageCount": 48,
            "description": 'Thorgal Aegirson est en mauvaise posture : il est enchaîné à '
                           'un rocher et est condamné à mourir, noyé par la marée '
                           "montante. Son crime est d'avoir osé aimer Aaricia, la fille du "
                           "roi des Vikings du Nord, lui, le bâtard né d'on ne sait qui et "
                           'on ne sait où. Il doit son salut à une magicienne qui le sauve '
                           'en échange de son obéissance...',
            "industryIdentifiers": _isbn_identifiers(THORGAL_ISBN),
            "language": "fr",
        },
    }),
    SAULE_ISBN: _volumes({
        "id": "sAuLe01AAAAJ",
        "volumeInfo": {
            "title": "Le bois sauvage",
            "authors": ["Michel Plessix", "Kenneth Grahame"],
            "publisher": "Productions Guy Delcourt",
            "publishedDate": "1999-08-23",
            "pageCount": 32,
            "description": "Adaptation en bande dessinée du roman de Kenneth Grahame "
                           "\"Le Vente dans les saules\".",
            "industryIdentifiers": _isbn_identifiers(SAULE_ISBN),
            "language": "fr",
        },
    }),
    BOVARY_ISBN: _volumes({
        "id": "1ThlAAAAMAAJ",
        "volumeInfo": {
            "title": "Madame Bovary",
            "authors": ["Gustave Flaubert", "Thierry Laget"],
            "publisher": "Gallimard Education",
            "publishedDate": "2001",
            "pageCount": 532,
            "categories": ["Fiction"],
            "language": "fr",
            "description": "Fille d'un riche fermier, Emma Rouault épouse Charles Bovary, "
                           "officier de santé et veuf récent d'une femme tyrannique. Élevée "
                           'dans un couvent, Emma aspire à vivre dans le monde de rêve dont '
                           "parlent les romans à l'eau de rose qu'elle y a lu. Un bal au "
                           "château de Vaubyessard la persuade qu'un tel monde existe, mais "
                           "le décalage qu'elle découvre avec sa propre vie déclenche chez "
                           "elle une maladie nerveuse. La naissance d'une fille la distrait "
                           'un peu, mais bientôt Emma cède aux avances de Rodolphe. Elle '
                           "veut s'enfuir avec son amant qui, lâche, l'abandonne... [RERO]",
            "industryIdentifiers": _isbn_identifiers(BOVARY_ISBN),
            "imageLinks": _cover("1ThlAAAAMAAJ"),
        },
    }),
}

EMPTY_RESPONSE = {"kind": "books#volumes", "totalItems": 0}


def fake_google_books_get(url: str, params: dict, **kwargs) -> MagicMock:
    """Remplace `requests.get` : renvoie la réponse enregistrée pour l'ISBN demandé."""
    isbn = int(params["q"].removeprefix("isbn:"))
    response = MagicMock(status_code=200)
    response.json.return_value = GOOGLE_BOOKS_RESPONSES.get(isbn, EMPTY_RESPONSE)
    return response


def http_error_response(status_code: int, text: str) -> MagicMock:
    return MagicMock(status_code=status_code, text=text)
