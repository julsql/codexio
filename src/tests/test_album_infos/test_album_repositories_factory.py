import unittest

from main.core.domain.model.profile_type import ProfileType
from main.core.infrastructure.api.album_repositories_factory import available_sources, build_album_repositories
from main.core.infrastructure.api.bd_gest_adapter import BdGestAdapter
from main.core.infrastructure.api.bnf_adapter import BnfAdapter
from tests.test_common.internal.logger_in_memory import LoggerInMemory


class TestAlbumRepositoriesFactory(unittest.TestCase):
    def setUp(self):
        self.logger = LoggerInMemory()

    def test_all_bd_sources_in_merge_order(self):
        repositories = build_album_repositories(ProfileType.BD, self.logger)

        self.assertEqual(
            ["BdPhileRepository", "BdGestRepository", "BdFugueRepository", "BdGoogleAdapter"],
            [str(repository) for repository in repositories],
        )

    def test_all_book_sources(self):
        repositories = build_album_repositories(ProfileType.BOOK, self.logger)

        self.assertEqual(3, len(repositories))

    def test_single_bd_source(self):
        repositories = build_album_repositories(ProfileType.BD, self.logger, "bdgest")

        self.assertEqual(1, len(repositories))
        self.assertIsInstance(repositories[0], BdGestAdapter)

    def test_single_book_source(self):
        repositories = build_album_repositories(ProfileType.BOOK, self.logger, "bnf")

        self.assertEqual(1, len(repositories))
        self.assertIsInstance(repositories[0], BnfAdapter)

    def test_unknown_source_returns_nothing(self):
        self.assertEqual([], build_album_repositories(ProfileType.BD, self.logger, "inconnu"))

    def test_source_of_another_profile_returns_nothing(self):
        """Une source livre ne doit pas être interrogeable depuis un profil BD"""
        self.assertEqual([], build_album_repositories(ProfileType.BD, self.logger, "bnf"))

    def test_available_sources(self):
        self.assertEqual(["bdphile", "bdgest", "bdfugue", "bdgoogle"], available_sources(ProfileType.BD))
        self.assertEqual(["googlebooks", "bnf", "openlibrary"], available_sources(ProfileType.BOOK))


if __name__ == "__main__":
    unittest.main()
