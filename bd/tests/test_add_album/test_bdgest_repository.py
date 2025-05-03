import unittest

from main.core.add_album.add_album_error import AddAlbumError
from main.core.add_album.internal.bdgest_connexion import BdGestRepository
from tests.album_data_set import ASTERIX_ISBN, ASTERIX_URLS, ASTERIX_DATA


class TestBdGestRepository(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bd_repository = BdGestRepository()

    def test_get_correct_url_from_isbn(self) -> None:
        link = self.bd_repository.get_url(ASTERIX_ISBN)
        self.assertEqual(ASTERIX_URLS['BDGEST'], link)

    def test_get_correct_url_from_empty_isbn(self) -> None:
        with self.assertRaises(AddAlbumError):
            self.bd_repository.get_url(0)

    def test_get_no_infos_from_empty_isbn(self) -> None:
        with self.assertRaises(AddAlbumError):
            self.bd_repository.get_infos(0)

    def test_get_correct_infos_from_asterix_isbn(self) -> None:
        infos = self.bd_repository.get_infos(ASTERIX_ISBN)
        self.assertEqual(ASTERIX_DATA['BDGEST'], infos)

    def test_get_correct_infos_from_sambre_isbn(self) -> None:
        infos = self.bd_repository.get_infos(9782754801096)
        self.assertEqual({
            'Album': "Chapitre 3 - Hiver 1831 : la lune qui regarde",
            'Série': "La guerre des Sambre - Hugo & Iris",
            'Numéro': "3",
            'Scénario': "Yslaire",
            'Dessin': "Jean Bastide,Vincent Mézil",
            'Couleurs': "Jean Bastide,Vincent Mézil",
            'Éditeur': "Futuropolis / Glénat",
            'Date de publication': "2009-11-25",
            'Pages': 56,
            'Prix': 15.5,
            'Synopsis': "Avec Hugo et Iris, Yslaire, revient sur la jeunesse d'Hugo "
                        "Sambre, le père de Bernard Sambre, sur l'écriture de son "
                        'manuscrit La guerre des yeux, sur sa passion funeste pour Iris, '
                        'mère de Julie, qui le mène au suicide. Ce troisième tome clôt de '
                        'façon magistrale ce premier cycle de La Guerre des Sambre !<br '
                        '/>\n'
                        'Hiver 1931. À la Bastide, la mort des parents Sambre laisse une '
                        "maison vide et ses occupants solitaires. Blanche, l'épouse "
                        "délaissée, s'échappe de cette atmosphère pesante en compagnie "
                        "d'un 'cousin' plus joyeux. Les soeurs d'Hugo portent le deuil "
                        "dans un silence réprobateur. Hugo Sambre s'occupe pour la "
                        'première fois de sa fille Sarah, en lui faisant la lecture du '
                        "manuscrit de La guerre des yeux. L'annonce du retour d'Iris à "
                        "Paris, l'actrice aux yeux rouges qui l'a envoûté, décide Hugo à "
                        'quitter précipitamment la Bastide, dans l?espoir de la '
                        'retrouver?<br />\n',
            'Image': "https://www.bedetheque.com/media/Couvertures/Couv_98900.jpg"
        }, infos)


if __name__ == '__main__':
    unittest.main()
