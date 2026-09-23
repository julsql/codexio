from dataclasses import fields
from datetime import date
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
    result = {}
    for field in fields(Album):
        value = getattr(album, field.name)
        if isinstance(value, date):
            result[field.name] = value.isoformat()
        elif isinstance(value, Decimal):
            result[field.name] = float(value)
        else:
            result[field.name] = value
    return result
