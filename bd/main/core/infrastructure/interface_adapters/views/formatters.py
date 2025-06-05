from decimal import Decimal
from typing import Optional

FLOAT_SEP = ","


def convert_price(price: Decimal) -> Optional[int | str]:
    if price:
        return int(price) if price == price.to_integral_value() else str(float(price)).replace(".", FLOAT_SEP)
    else:
        return None
