from main.core.add_album.add_album_error import AddAlbumError
from main.core.add_album.bd_repository import BdRepository


class BdInMemory(BdRepository):

    def __init__(self, name: str, data: dict) -> None:
        self.name = name
        self.data = {int(data.get('ISBN', '0')): data}

    def get_infos(self, isbn: int) -> dict:
        if isbn in self.data:
            return self.data[isbn]
        else:
            raise AddAlbumError(f"Aucun album trouvé avec l'isbn {isbn}")

    def get_url(self, isbn: int) -> str:
        return f"http://mock-{self.name}.com/{isbn}"

    def get_html(self, url: str) -> str:
        return "<html><body><h1>Mock</h1></body></html>"

    def __str__(self) -> str:
        return self.name
