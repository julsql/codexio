import unittest

from main.core.application.usecases.add_album.get_infos_service import GetInfosService
from main.core.domain.exceptions.album_exceptions import AlbumNotFoundException, \
    AlbumSourcesUnavailableException
from main.core.domain.exceptions.api_exceptions import ApiConnexionDataNotFound, ApiConnexionException
from main.core.domain.model.album import Album
from main.core.domain.ports.repositories.add_album_repository import AddAlbumRepository
from tests.album_data_set import ASTERIX
from tests.test_add_album.album_large_data_set import ASTERIX_ISBN
from tests.test_add_album.internal.bd_in_memory import AddAlbumInMemory
from tests.test_common.internal.logger_in_memory import LoggerInMemory


class DataNotFoundRepository(AddAlbumRepository):
    """Source joignable qui ne connaît pas l'ISBN"""

    def __init__(self, name: str) -> None:
        self.name = name

    def get_infos(self, isbn: int) -> Album:
        raise ApiConnexionDataNotFound("introuvable", self.name, isbn)

    def __str__(self) -> str:
        return self.name


class UnreachableRepository(AddAlbumRepository):
    """Source en panne : quota dépassé, 403, réseau coupé..."""

    def __init__(self, name: str) -> None:
        self.name = name

    def get_infos(self, isbn: int) -> Album:
        raise ApiConnexionException("429 Quota exceeded", self.name, isbn)

    def __str__(self) -> str:
        return self.name


class TestGetInfosFailures(unittest.TestCase):
    def setUp(self):
        self.logger = LoggerInMemory()

    def test_all_sources_know_nothing_is_not_found(self):
        """Toutes les sources répondent mais aucune ne connaît l'ISBN : 404 attendu"""
        service = GetInfosService(
            [DataNotFoundRepository("source1"), DataNotFoundRepository("source2")],
            self.logger,
        )

        with self.assertRaises(AlbumNotFoundException):
            service.main(ASTERIX_ISBN)

    def test_all_sources_broken_is_unavailable(self):
        """Toutes les sources sont en panne : ce n'est pas un ISBN introuvable"""
        service = GetInfosService(
            [UnreachableRepository("bdgoogle"), UnreachableRepository("bnf")],
            self.logger,
        )

        with self.assertRaises(AlbumSourcesUnavailableException) as context:
            service.main(ASTERIX_ISBN)

        self.assertEqual(["bdgoogle", "bnf"], context.exception.sources)

    def test_only_broken_sources_are_reported(self):
        """Une source qui ignore l'ISBN n'est pas comptée comme en panne"""
        service = GetInfosService(
            [DataNotFoundRepository("bdphile"), UnreachableRepository("bdgoogle")],
            self.logger,
        )

        with self.assertRaises(AlbumSourcesUnavailableException) as context:
            service.main(ASTERIX_ISBN)

        self.assertEqual(["bdgoogle"], context.exception.sources)

    def test_a_broken_source_does_not_hide_a_working_one(self):
        """Une panne sur une source ne doit pas empêcher de renvoyer les données des autres"""
        service = GetInfosService(
            [UnreachableRepository("bdgoogle"), AddAlbumInMemory("bdphile", ASTERIX)],
            self.logger,
        )

        album = service.main(ASTERIX_ISBN)

        self.assertEqual(ASTERIX.title, album.title)


if __name__ == "__main__":
    unittest.main()
