from main.core.random_album.internal.random_album_connexion import RandomAlbumConnexion


class RandomAlbumService:
    def __init__(self, random_alnum_repository: RandomAlbumConnexion) -> None:
        self.connexion = random_alnum_repository

    def main(self) -> dict[str, str]:
        return self.connexion.get_random_album()
