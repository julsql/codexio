import unittest

from main.core.add_album.get_infos_service import GetInfosService


class TestCorrectInfos(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.service = GetInfosService(0, [])

    def test_get_correct_info_successfully(self):
        info = self.service.corriger_info({})
        self.assertEqual({
            'Album': '', 'Couleurs': '', 'Date de publication': '',
            'Dessin': '', 'Édition': '', 'ISBN': '', 'Image': '',
            'Numéro': '', 'Pages': '', 'Prix': '', 'Scénario': '',
            'Synopsis': '', 'Série': '', 'Éditeur': ''},
            info)

    def test_raise_error_correct_empty_value(self):
        with self.assertRaises(AttributeError):
            self.service.corriger_info("")


if __name__ == '__main__':
    unittest.main()
