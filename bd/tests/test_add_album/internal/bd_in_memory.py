from main.core.domain.exceptions.album_exceptions import AlbumNotFoundException
from main.core.domain.model.album import Album
from main.core.domain.model.book import Book
from main.core.domain.ports.repositories.add_album_repository import AddAlbumRepository


class AddAlbumInMemory(AddAlbumRepository):

    def __init__(self, name: str, data: Album | Book) -> None:
        self.name = name
        self.data = {data.isbn: data}
        self.isbn = 0

    def get_infos(self, isbn: int) -> Album | Book:
        self.isbn = isbn
        if isbn in self.data:
            return self.data[isbn]
        else:
            raise AlbumNotFoundException(f"Aucun album trouvé avec l'isbn {isbn}", isbn)

    def get_url(self, ) -> str:
        return f"http://mock-{self.name}.com/{self.isbn}"

    def get_html(self, url: str) -> str:
        return "<html><body><h1>Mock</h1></body></html>"

    def __str__(self) -> str:
        return self.name
