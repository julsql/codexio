import unittest

from main.core.add_album.add_album_error import AddAlbumError
from main.core.add_album.internal.bdphile_connexion import BdPhileRepository
from tests.album_data_set import ASTERIX_ISBN, ASTERIX_URLS, ASTERIX_DATA


class TestBdPhileRepository(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bd_repository = BdPhileRepository()

    def test_get_correct_url_from_isbn(self) -> None:
        link = self.bd_repository.get_url(ASTERIX_ISBN)
        self.assertEqual(ASTERIX_URLS['BDPHILE'], link)

    def test_get_correct_url_from_empty_isbn(self) -> None:
        with self.assertRaises(AddAlbumError):
            self.bd_repository.get_url(0)

    def test_get_no_infos_from_empty_isbn(self) -> None:
        with self.assertRaises(AddAlbumError):
            self.bd_repository.get_infos(0)

    def test_get_correct_infos_from_asterix_isbn(self) -> None:
        infos = self.bd_repository.get_infos(ASTERIX_ISBN)
        self.assertEqual(ASTERIX_DATA['BDPHILE'], infos)

    def test_get_correct_infos_from_sambre_isbn(self) -> None:
        infos = self.bd_repository.get_infos(9782754801096)
        self.assertEqual({
            'Album': "Hiver 1831 - La Lune qui regarde",
            'Série': "La Guerre des Sambre - Hugo & Iris",
            'Numéro': "3",
            'Scénario': "Yslaire (Bernard Hislaire)",
            'Dessin': "Jean Bastide,Vincent Mézil",
            'Éditeur': "Futuropolis - Glénat",
            'Édition': "1 réédition",
            'Date de publication': "2009-11-25",
            'Pages': 56,
            'Prix': 14.0,
            'Synopsis': 'Hiver 1831. À la Bastide, la mort des parents Sambre laisse une '
                        "maison vide et ses occupants solitaires. Blanche, l'épouse "
                        "délaissée, s'échappe de cette atmosphère pesante en compagnie "
                        "d'un \x93 cousin \x94 plus joyeux. Les sœurs d'Hugo portent le "
                        "deuil dans un silence réprobateur. Hugo Sambre s'occupe pour la "
                        'première fois de sa fille Sarah, en lui faisant la lecture du '
                        "manuscrit de La guerre des yeux. L'annonce du retour d'Iris à "
                        "Paris, l'actrice aux yeux rouges qui l'a envoûté, décide Hugo à "
                        "quitter précipitamment la Bastide, dans l'espoir de la retrouver",
            'Image': "https://static.bdphile.fr/images/media/cover/0005/5175.jpg"
        }, infos)


if __name__ == '__main__':
    unittest.main()
