from main.core.random_album.internal.random_album_connexion import RandomAlbumConnexion
from main.core.random_album.random_album_service import RandomAlbumService


def random_album() -> dict[str, str]:
    random_album_connexion = RandomAlbumConnexion()
    service = RandomAlbumService(random_album_connexion)
    return service.main()
