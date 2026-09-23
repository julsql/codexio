from decimal import Decimal
from typing import Optional

from main.core.domain.model.album import Album

FLOAT_SEP = ","


def convert_price(price: Decimal) -> Optional[int | str]:
    if price:
        return int(price) if price == price.to_integral_value() else str(float(price)).replace(".", FLOAT_SEP)
    else:
        return None


def album_to_dict(album: Album) -> dict:
    """Convertit un objet Album en dictionnaire sérialisable en JSON"""
    return {
        "isbn": album.isbn,
        "title": album.title,
        "number": album.number,
        "series": album.series,
        "writer": album.writer,
        "illustrator": album.illustrator,
        "translator": album.translator,
        "colorist": album.colorist,
        "publisher": album.publisher,
        "collection_book": album.collection_book,
        "literary_genre": album.literary_genre,
        "style": album.style,
        "origin_language": album.origin_language,
        "publication_date": album.publication_date.isoformat() if album.publication_date else None,
        "edition": album.edition,
        "number_of_pages": album.number_of_pages,
        "purchase_price": float(album.purchase_price) if album.purchase_price else None,
        "synopsis": album.synopsis,
        "image": album.image,
    }
