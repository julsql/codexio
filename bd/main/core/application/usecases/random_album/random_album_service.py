from django.contrib.auth.base_user import AbstractBaseUser

from main.core.domain.model.album import Album
from main.core.domain.ports.repositories.random_album_repository import RandomAlbumRepository


class RandomAlbumService:
    def __init__(self, random_album_repository: RandomAlbumRepository) -> None:
        self.connexion = random_album_repository

    def main(self, user: AbstractBaseUser) -> Album:
        return self.connexion.get_random_album(user)
