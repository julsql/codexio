import dataclasses
import os
import unittest

from main.core.domain.exceptions.api_exceptions import ApiConnexionDataNotFound
from main.core.domain.model.album import Album
from main.core.infrastructure.api.bd_fugue_adapter import BdFugueAdapter
from tests.test_add_album.album_large_data_set import ASTERIX_ISBN, ASTERIX_URLS, ASTERIX_DATA, SAMBRE_ISBN, \
    SAMBRE_DATA, THORGAL_ISBN, THORGAL_DATA, SAULE_ISBN, SAULE_DATA
from tests.test_common.internal.logger_in_memory import LoggerInMemory


@unittest.skipIf(
    os.getenv("CI") or os.getenv("GITHUB_ACTIONS"),
    "Cloudflare bloque les IPs des runners GitHub Actions (HTTP 403)",
)
class TestBdFugueRepository(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.logging_repository = LoggerInMemory()
        cls.bd_repository = BdFugueAdapter(cls.logging_repository)

    def assertAlbumEqual(self, expected: Album, actual: Album) -> None:
        # Le prix affiché par bdfugue.com bouge au fil des promotions :
        # on vérifie qu'un prix est bien extrait, pas sa valeur exacte.
        self.assertIsNotNone(actual.purchase_price)
        self.assertEqual(
            dataclasses.replace(expected, purchase_price=None),
            dataclasses.replace(actual, purchase_price=None),
        )

    def test_get_correct_url_from_isbn(self) -> None:
        self.bd_repository.isbn = ASTERIX_ISBN
        link = self.bd_repository.get_url()
        self.assertEqual(ASTERIX_URLS['BDFUGUE'], link)

    def test_get_no_infos_from_empty_isbn(self) -> None:
        with self.assertRaises(ApiConnexionDataNotFound):
            self.bd_repository.get_infos(0)

    def test_get_correct_infos_from_isbn(self) -> None:
        infos = self.bd_repository.get_infos(ASTERIX_ISBN)
        self.assertAlbumEqual(ASTERIX_DATA['BDFUGUE'], infos)

    def test_get_correct_infos_from_sambre_isbn(self) -> None:
        infos = self.bd_repository.get_infos(SAMBRE_ISBN)
        self.assertAlbumEqual(SAMBRE_DATA['BDFUGUE'], infos)

    def test_get_correct_infos_from_thorgal_isbn(self) -> None:
        infos = self.bd_repository.get_infos(THORGAL_ISBN)
        self.assertAlbumEqual(THORGAL_DATA['BDFUGUE'], infos)

    def test_get_correct_infos_from_saule_isbn(self) -> None:
        infos = self.bd_repository.get_infos(SAULE_ISBN)
        self.assertAlbumEqual(SAULE_DATA['BDFUGUE'], infos)


if __name__ == '__main__':
    unittest.main()
