import unittest

from main.add_album import error
from main.add_album import sheet_add_album
from main.add_album.sheet_connection import Conn


class TestIntegration(unittest.TestCase):

    def setUp(self):
        self.logs = "logs-test-unit.txt"
        self.doc_name = "bd"
        self.sheet = "Test"
        self.isbn = 9782864976165
        self.asterix = {
            'Album': 'Astérix (Albums des films)',
            'Couleurs': 'Thierry Mébarki',
            'Date de publication': '2023-02-08',
            'Dessin': 'Fabrice Tarrin',
            'ISBN': 9782864976165,
            'Image': 'https://static.bdphile.info/images/media/cover/160391.jpg',
            'Numéro': '10',
            'Pages': 48,
            'Prix': 10.5,
            'Scénario': 'Olivier Gay',
            'Synopsis': 'Nous sommes en 50 av J.-C. Loin, très loin du petit village '
                        "d'Armorique que nous connaissons bien, l'Impératrice de Chine "
                        "est emprisonnée suite à coup d'état fomenté par l'infâme Deng "
                        "Tsin Qin.<br/>La princesse Fu Yi, fille unique de l'Impératrice, "
                        'aidée par sa fidèle guerrière Tat Han et Graindemaïs, le neveu '
                        "du marchand phénicien Epidemaïs, s'enfuit pour demander de "
                        "l'aide aux Irréductibles Gaulois.",
            'Série': "L'empire du milieu",
            'Éditeur': 'Albert René',
            'Édition': 'Édition originale Noté : Impression en décembre 2022 - n° '
                       '616-5-01 Impression et reliure par Pollina - n°13651'}

    def tearDown(self):
        pass

    def test_liste_from_dict_pass_1(self):
        liste = sheet_add_album.liste_from_dict({
            'Album': '', 'Couleurs': '', 'Date de publication': '',
            'Dessin': '', 'Édition': '', 'ISBN': '', 'Image': '',
            'Numéro': '', 'Pages': '', 'Prix': '', 'Scénario': '',
            'Synopsis': '', 'Série': '', 'Éditeur': ''})
        self.assertEqual(liste, [""] * 19)

    def test_liste_from_dict_pass_2(self):
        liste = sheet_add_album.liste_from_dict({
            'Album': 'a', 'Couleurs': 'a', 'Date de publication': 'a',
            'Dessin': 'a', 'Édition': 'a', 'ISBN': 'a', 'Image': 'a',
            'Numéro': 'a', 'Pages': 'a', 'Prix': 'a', 'Scénario': 'a',
            'Synopsis': 'a', 'Série': 'a', 'Éditeur': 'a'})
        self.assertEqual(liste,
                         ["a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "", "a", "", "", "", "", "a", "a"])

    def test_liste_from_dict_fail(self):
        with self.assertRaises(IndexError):
            sheet_add_album.liste_from_dict({})

    def test_add_pass(self):
        self.assertEqual(sheet_add_album.add(self.isbn, self.doc_name, self.sheet, self.logs), self.asterix)
        connection = Conn()
        connection.open(self.doc_name, self.sheet)
        sheet_line = connection.get_line(0)
        self.assertEqual(sheet_line, [
            '9782864976165',
            'Astérix (Albums des films)',
            '10',
            "L'empire du milieu",
            'Olivier Gay',
            'Fabrice Tarrin',
            'Thierry Mébarki',
            'Albert René',
            '2023-02-08',
            'Édition originale Noté : Impression en décembre 2022 - n° 616-5-01 '
            'Impression et reliure par Pollina - n°13651',
            '48',
            '',
            '10,5',
            '',
            '',
            '',
            '',
            "Nous sommes en 50 av J.-C. Loin, très loin du petit village d'Armorique que "
            "nous connaissons bien, l'Impératrice de Chine est emprisonnée suite à coup "
            "d'état fomenté par l'infâme Deng Tsin Qin.<br/>La princesse Fu Yi, fille "
            "unique de l'Impératrice, aidée par sa fidèle guerrière Tat Han et "
            "Graindemaïs, le neveu du marchand phénicien Epidemaïs, s'enfuit pour "
            "demander de l'aide aux Irréductibles Gaulois.",
            'https://static.bdphile.info/images/media/cover/160391.jpg'])

        connection.set_line([""] * 19, 0)

        sheet_content = connection.get_all()
        self.assertEqual(sheet_content, [])

    def test_add_fail_1(self):
        with self.assertRaises(error.Error):
            sheet_add_album.add(self.isbn, "youhou", None, self.logs)

    def test_add_fail_2(self):
        with self.assertRaises(error.Error):
            sheet_add_album.add(self.isbn, self.doc_name, "sheet", self.logs)

    def test_add_fail_3(self):
        sheet_add_album.add(self.isbn, self.doc_name, self.sheet, self.logs)

        with self.assertRaises(error.Error):
            sheet_add_album.add(self.isbn, self.doc_name, self.sheet, self.logs)

        connection = Conn()
        connection.open(self.doc_name, self.sheet)
        connection.set_line([""] * 19, 0)

        sheet_content = connection.get_all()
        self.assertEqual(sheet_content, [])


if __name__ == '__main__':
    unittest.main()
