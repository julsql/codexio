from main.core.domain.model.album import Album
from main.core.domain.ports.repositories.add_album_repository import AddAlbumRepository
from main.core.domain.ports.repositories.album_cache_repository import AlbumCacheRepository


class CachedAlbumRepository(AddAlbumRepository):
    """Sert la notice mémorisée d'une source si elle existe, sinon interroge la source et la mémorise

    Seuls les succès sont mémorisés : une panne ou un ISBN inconnu laisse le cache intact,
    pour ne jamais figer un échec.
    """

    def __init__(self, repository: AddAlbumRepository, cache_repository: AlbumCacheRepository) -> None:
        self.repository = repository
        self.cache_repository = cache_repository

    def get_infos(self, isbn: int) -> Album:
        source = str(self.repository)

        cached = self.cache_repository.get(source, isbn)
        if cached is not None:
            return cached

        album = self.repository.get_infos(isbn)
        self.cache_repository.save(source, isbn, album)
        return album

    def __str__(self) -> str:
        return str(self.repository)
