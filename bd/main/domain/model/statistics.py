from dataclasses import dataclass


@dataclass
class Statistics:
    albums_count: int
    pages_count: int
    purchase_price_count: float
    deluxe_edition_count: int
    signed_copies_count: int
    ex_libris_count: int

    @classmethod
    def empty(cls) -> 'Statistics':
        return cls(0, 0, 0.0, 0, 0, 0)

    def __str__(self):
        return f"Statistics(albums_count={self.albums_count}, pages_count={self.pages_count}, " \
               f"purchase_price_count={self.purchase_price_count}, deluxe_edition_count={self.deluxe_edition_count}, " \
               f"signed_copies_count={self.signed_copies_count}, ex_libris_count={self.ex_libris_count})"