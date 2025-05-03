from main.core.random_album.random_album_repository import RandomAlbumRepository


class RandomAlbumService:
    def __init__(self, random_album_repository: RandomAlbumRepository) -> None:
        self.connexion = random_album_repository

    def main(self) -> dict[str, str]:
        return self.connexion.get_random_album()
