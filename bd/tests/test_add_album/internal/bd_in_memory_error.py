from main.core.add_album.add_album_error import AddAlbumError
from main.core.add_album.bd_repository import BdRepository


class BdInMemoryError(BdRepository):
    def __init__(self, name: str) -> None:
        self.name = name

    def get_infos(self, isbn: int) -> dict:
        return {}

    def get_url(self, isbn: int) -> str:
        return f"http://mock-{self.name}.com/{isbn}"

    def get_html(self, url: str) -> str:
        raise AddAlbumError(f"Impossible d'affiche le code html de la page {url}")

    def __str__(self) -> str:
        return self.name
