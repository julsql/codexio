import dataclasses
import re
import unittest

from main.core.domain.exceptions.api_exceptions import ApiConnexionDataNotFound
from main.core.domain.model.album import Album
from main.core.infrastructure.api.bd_phile_adapter import BdPhileAdapter
from tests.test_add_album.album_large_data_set import ASTERIX_ISBN, ASTERIX_URLS, ASTERIX_DATA, SAMBRE_ISBN, \
    SAMBRE_DATA, \
    THORGAL_ISBN, THORGAL_DATA, SAULE_ISBN, SAULE_DATA
from tests.test_common.internal.logger_in_memory import LoggerInMemory

# BDPhile incrémente son compteur de rééditions au fil des republications :
# la valeur exacte dépend de la date d'exécution du test, on la neutralise.
REEDITIONS_PATTERN = re.compile(r"\d+ rééditions")


def _without_reeditions_count(album: Album) -> Album:
    return dataclasses.replace(album, edition=REEDITIONS_PATTERN.sub("N rééditions", album.edition))


class TestBdPhileRepository(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.logging_repository = LoggerInMemory()
        cls.bd_repository = BdPhileAdapter(cls.logging_repository)

    def assertAlbumEqual(self, expected: Album, actual: Album) -> None:
        self.assertEqual(_without_reeditions_count(expected), _without_reeditions_count(actual))

    def test_get_correct_url_from_isbn(self) -> None:
        self.bd_repository.isbn = ASTERIX_ISBN
        link = self.bd_repository.get_url()
        self.assertEqual(ASTERIX_URLS['BDPHILE'], link)

    def test_get_correct_url_from_empty_isbn(self) -> None:
        self.bd_repository.isbn = 0
        with self.assertRaises(ApiConnexionDataNotFound):
            self.bd_repository.get_url()

    def test_get_no_infos_from_empty_isbn(self) -> None:
        with self.assertRaises(ApiConnexionDataNotFound):
            self.bd_repository.get_infos(0)

    def test_get_correct_infos_from_asterix_isbn(self) -> None:
        infos = self.bd_repository.get_infos(ASTERIX_ISBN)
        self.assertAlbumEqual(ASTERIX_DATA['BDPHILE'], infos)

    def test_get_correct_infos_from_sambre_isbn(self) -> None:
        infos = self.bd_repository.get_infos(SAMBRE_ISBN)
        self.assertAlbumEqual(SAMBRE_DATA['BDPHILE'], infos)

    def test_get_correct_infos_from_thorgal_isbn(self) -> None:
        infos = self.bd_repository.get_infos(THORGAL_ISBN)
        self.assertAlbumEqual(THORGAL_DATA['BDPHILE'], infos)

    def test_get_correct_infos_from_saule_isbn(self) -> None:
        infos = self.bd_repository.get_infos(SAULE_ISBN)
        self.assertAlbumEqual(SAULE_DATA['BDPHILE'], infos)


if __name__ == '__main__':
    unittest.main()
