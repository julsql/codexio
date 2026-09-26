import unittest

from main.core.domain.exceptions.api_exceptions import ApiConnexionDataNotFound, ApiConnexionException
from main.core.domain.model.album import Album
from main.core.domain.ports.repositories.add_album_repository import AddAlbumRepository
from main.core.infrastructure.api.cached_album_repository import CachedAlbumRepository
from tests.album_data_set import ASTERIX
from tests.test_add_album.album_large_data_set import ASTERIX_ISBN
from tests.test_common.internal.album_cache_in_memory import AlbumCacheInMemory


class CountingRepository(AddAlbumRepository):
    def __init__(self, album: Album) -> None:
        self.album = album
        self.calls = 0

    def get_infos(self, isbn: int) -> Album:
        self.calls += 1
        return self.album

    def __str__(self) -> str:
        return "bdphile"


class FailingRepository(AddAlbumRepository):
    def __init__(self, error: Exception) -> None:
        self.error = error
        self.calls = 0

    def get_infos(self, isbn: int) -> Album:
        self.calls += 1
        raise self.error

    def __str__(self) -> str:
        return "bdfugue"


class TestCachedAlbumRepository(unittest.TestCase):
    def setUp(self):
        self.cache = AlbumCacheInMemory()

    def test_first_call_queries_the_source(self):
        source = CountingRepository(ASTERIX)
        repository = CachedAlbumRepository(source, self.cache)

        album = repository.get_infos(ASTERIX_ISBN)

        self.assertEqual(ASTERIX.title, album.title)
        self.assertEqual(1, source.calls)
        self.assertEqual(1, self.cache.writes)

    def test_second_call_does_not_query_the_source(self):
        source = CountingRepository(ASTERIX)
        repository = CachedAlbumRepository(source, self.cache)

        repository.get_infos(ASTERIX_ISBN)
        album = repository.get_infos(ASTERIX_ISBN)

        self.assertEqual(ASTERIX.title, album.title)
        self.assertEqual(1, source.calls, "la source ne doit être interrogée qu'une fois")
        self.assertEqual(1, self.cache.writes)

    def test_another_isbn_still_queries_the_source(self):
        source = CountingRepository(ASTERIX)
        repository = CachedAlbumRepository(source, self.cache)

        repository.get_infos(ASTERIX_ISBN)
        repository.get_infos(9999999999999)

        self.assertEqual(2, source.calls)

    def test_a_failure_is_never_cached(self):
        """Mémoriser une panne la figerait jusqu'à expiration du cache"""
        source = FailingRepository(ApiConnexionException("403", "bdfugue", ASTERIX_ISBN))
        repository = CachedAlbumRepository(source, self.cache)

        with self.assertRaises(ApiConnexionException):
            repository.get_infos(ASTERIX_ISBN)

        self.assertEqual(0, self.cache.writes)

    def test_an_unknown_isbn_is_never_cached(self):
        source = FailingRepository(ApiConnexionDataNotFound("introuvable", "bdfugue", ASTERIX_ISBN))
        repository = CachedAlbumRepository(source, self.cache)

        with self.assertRaises(ApiConnexionDataNotFound):
            repository.get_infos(ASTERIX_ISBN)

        self.assertEqual(0, self.cache.writes)

    def test_keeps_the_source_name(self):
        """GetInfosService et ?source= identifient les sources par leur nom"""
        repository = CachedAlbumRepository(CountingRepository(ASTERIX), self.cache)

        self.assertEqual("bdphile", str(repository))

    def test_entries_are_isolated_per_source(self):
        first = CountingRepository(ASTERIX)
        second = FailingRepository(ApiConnexionException("403", "bdfugue", ASTERIX_ISBN))

        CachedAlbumRepository(first, self.cache).get_infos(ASTERIX_ISBN)

        # La notice de bdphile ne doit pas servir de réponse pour bdfugue
        with self.assertRaises(ApiConnexionException):
            CachedAlbumRepository(second, self.cache).get_infos(ASTERIX_ISBN)


if __name__ == "__main__":
    unittest.main()
