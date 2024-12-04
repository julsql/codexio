from main.core.add_album.add_album_error import AddAlbumError
from main.core.add_album.bd_repository import BdRepository
from tests.album_data_set import ASTERIX, ASTERIX_ISBN


class BdInMemory(BdRepository):
    def __init__(self):
        self.values = {ASTERIX_ISBN: ASTERIX}

    def get_infos(self, isbn: int) -> dict:
        if isbn in self.values:
            return self.values[isbn]
        else:
            raise AddAlbumError(f"Aucun album trouvé avec l'isbn {isbn}")

    def get_url(self, isbn: int):
        return ""
