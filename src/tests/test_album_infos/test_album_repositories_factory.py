import unittest

from main.core.domain.model.profile_type import ProfileType
from main.core.infrastructure.api.album_repositories_factory import available_sources, build_album_repositories
from main.core.infrastructure.api.bd_fugue_adapter import BdFugueAdapter
from main.core.infrastructure.api.bd_gest_adapter import BdGestAdapter
from main.core.infrastructure.api.bnf_adapter import BnfAdapter
from main.core.infrastructure.api.cached_album_repository import CachedAlbumRepository
from tests.test_common.internal.album_cache_in_memory import AlbumCacheInMemory
from tests.test_common.internal.logger_in_memory import LoggerInMemory


class TestAlbumRepositoriesFactory(unittest.TestCase):
    def setUp(self):
        self.logger = LoggerInMemory()

    def test_all_bd_sources_in_merge_order(self):
        repositories = build_album_repositories(ProfileType.BD, self.logger)

        self.assertEqual(
            ["BdPhileRepository", "BdGestRepository", "BdGoogleAdapter"],
            [str(repository) for repository in repositories],
        )

    def test_all_book_sources(self):
        repositories = build_album_repositories(ProfileType.BOOK, self.logger)

        self.assertEqual(3, len(repositories))

    def test_single_bd_source(self):
        repositories = build_album_repositories(ProfileType.BD, self.logger, "bdgest")

        self.assertEqual(1, len(repositories))
        self.assertIsInstance(repositories[0], BdGestAdapter)

    def test_on_demand_source_is_left_out_of_the_merge(self):
        repositories = build_album_repositories(ProfileType.BD, self.logger)

        self.assertFalse(any(isinstance(r, BdFugueAdapter) for r in repositories))

    def test_on_demand_source_can_still_be_queried_alone(self):
        repositories = build_album_repositories(ProfileType.BD, self.logger, "bdfugue")

        self.assertEqual(1, len(repositories))
        self.assertIsInstance(repositories[0], BdFugueAdapter)

    def test_single_book_source(self):
        repositories = build_album_repositories(ProfileType.BOOK, self.logger, "bnf")

        self.assertEqual(1, len(repositories))
        self.assertIsInstance(repositories[0], BnfAdapter)

    def test_unknown_source_returns_nothing(self):
        self.assertEqual([], build_album_repositories(ProfileType.BD, self.logger, "inconnu"))

    def test_source_of_another_profile_returns_nothing(self):
        """Une source livre ne doit pas être interrogeable depuis un profil BD"""
        self.assertEqual([], build_album_repositories(ProfileType.BD, self.logger, "bnf"))

    def test_without_cache_the_adapters_are_returned_as_is(self):
        repositories = build_album_repositories(ProfileType.BD, self.logger)

        self.assertFalse(any(isinstance(r, CachedAlbumRepository) for r in repositories))

    def test_with_a_cache_every_source_is_wrapped(self):
        repositories = build_album_repositories(ProfileType.BD, self.logger, None, AlbumCacheInMemory())

        self.assertEqual(3, len(repositories))
        self.assertTrue(all(isinstance(r, CachedAlbumRepository) for r in repositories))
        self.assertEqual(
            ["BdPhileRepository", "BdGestRepository", "BdGoogleAdapter"],
            [str(r) for r in repositories],
            "le nom de la source doit rester lisible à travers le cache",
        )

    def test_a_single_source_is_wrapped_too(self):
        repositories = build_album_repositories(ProfileType.BD, self.logger, "bdgest", AlbumCacheInMemory())

        self.assertEqual(1, len(repositories))
        self.assertIsInstance(repositories[0], CachedAlbumRepository)
        self.assertEqual("BdGestRepository", str(repositories[0]))

    def test_available_sources(self):
        self.assertEqual(["bdphile", "bdgest", "bdfugue", "bdgoogle"], available_sources(ProfileType.BD))
        self.assertEqual(["googlebooks", "bnf", "openlibrary"], available_sources(ProfileType.BOOK))


if __name__ == "__main__":
    unittest.main()
