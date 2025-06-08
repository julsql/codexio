from main.core.domain.model.album import Album
from main.core.domain.ports.repositories.random_album_repository import RandomAlbumRepository
from main.core.infrastructure.persistence.database.models import Collection


class RandomAlbumService:
    def __init__(self, random_album_repository: RandomAlbumRepository) -> None:
        self.connexion = random_album_repository

    def main(self, collection: Collection) -> Album:
        return self.connexion.get_random_album(collection)
