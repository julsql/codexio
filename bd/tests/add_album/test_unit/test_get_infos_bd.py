import datetime
import unittest

from main.add_album import error
from main.add_album import get_infos_bd


class TestGetInfosBd(unittest.TestCase):

    def setUp(self):
        self.logs = "logs-test-unit.txt"
        self.asterix = {
             'Album': "L'empire du milieu",
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
             'Série': 'Astérix (Albums des films)',
             'Éditeur': 'Albert René',
             'Édition': 'Édition originale Noté : Impression en décembre 2022 - n° '
                        '616-5-01 Impression et reliure par Pollina - n°13651'}

    def tearDown(self):
        pass

    def test_get_link_pass(self):
        link = get_infos_bd.get_link(9782840555698)
        self.assertEqual(link, "https://www.bdphile.fr/album/view/27231/")

    def test_get_link_fail(self):
        link = get_infos_bd.get_link("")
        self.assertEqual(link, 0)

    def test_corriger_info_pass(self):
        info = get_infos_bd.corriger_info({}, "")
        self.assertEqual(info, {
            'Album': '', 'Couleurs': '', 'Date de publication': '',
            'Dessin': '', 'Édition': '', 'ISBN': '', 'Image': '',
            'Numéro': '', 'Pages': '', 'Prix': '', 'Scénario': '',
            'Synopsis': '', 'Série': '', 'Éditeur': ''})

    def test_corriger_info_fail(self):
        with self.assertRaises(AttributeError):
            get_infos_bd.corriger_info("", "")

    def test_main_pass_1(self):
        info = get_infos_bd.main("9782864976165", self.logs)
        self.assertEqual(info, self.asterix)

    def test_main_pass_2(self):
        info = get_infos_bd.main(9782864976165, self.logs)
        self.assertEqual(info, self.asterix)

    def test_main_pass_3(self):
        get_infos_bd.main(9782756082332, self.logs)

    def test_main_fail_1(self):
        with self.assertRaises(error.Error):
            get_infos_bd.main("bonjour", self.logs)

    def test_main_fail_2(self):
        with self.assertRaises(error.Error):
            get_infos_bd.main("", self.logs)

    def test_main_fail_3(self):
        with self.assertRaises(error.Error):
            get_infos_bd.main(10001, self.logs)

    def test_parse_date_pass_1(self):
        date = get_infos_bd.parse_date("2021")
        self.assertEqual(date, datetime.date(2021, 1, 1).strftime("%Y-%m-%d"))

    def test_parse_date_pass_2(self):
        date = get_infos_bd.parse_date("3 FEVRIER 2021")
        self.assertEqual(date, datetime.date(2021, 2, 3).strftime("%Y-%m-%d"))

    def test_parse_date_pass_3(self):
        date = get_infos_bd.parse_date("3 FÉVRIER 2021")
        self.assertEqual(date, datetime.date(2021, 2, 3).strftime("%Y-%m-%d"))

    def test_parse_date_pass_4(self):
        date = get_infos_bd.parse_date("aout 2021")
        self.assertEqual(date, datetime.date(2021, 8, 1).strftime("%Y-%m-%d"))

    def test_parse_date_pass_5(self):
        date = get_infos_bd.parse_date("4th March 2021")
        self.assertEqual(date, datetime.date(2021, 3, 4).strftime("%Y-%m-%d"))

    def test_parse_date_pass_6(self):
        date = get_infos_bd.parse_date("April, 2nd 2021")
        self.assertEqual(date, datetime.date(2021, 4, 2).strftime("%Y-%m-%d"))

    def test_parse_date_pass_7(self):
        date = get_infos_bd.parse_date("février 2021")
        self.assertEqual(date, datetime.date(2021, 2, 1).strftime("%Y-%m-%d"))

    def test_parse_date_pass_8(self):
        date = get_infos_bd.parse_date("2021 Septembre 4e")
        self.assertEqual(date, datetime.date(2021, 9, 4).strftime("%Y-%m-%d"))

    def test_parse_date_pass_9(self):
        date = get_infos_bd.parse_date("13/11/2021")
        self.assertEqual(date, datetime.date(2021, 11, 13).strftime("%Y-%m-%d"))

    def test_parse_date_pass_10(self):
        date = get_infos_bd.parse_date("2021/04/30")
        self.assertEqual(date, datetime.date(2021, 4, 30).strftime("%Y-%m-%d"))

    def test_parse_date_pass_11(self):
        date = get_infos_bd.parse_date("10 02 2021")
        self.assertEqual(date, datetime.date(2021, 2, 10).strftime("%Y-%m-%d"))

    def test_parse_date_fail_1(self):
        date_str = "BRUH"
        date = get_infos_bd.parse_date(date_str)
        self.assertEqual(date, date_str)

    def test_parse_date_fail_2(self):
        date_str = ""
        date = get_infos_bd.parse_date(date_str)
        self.assertEqual(date, date_str)

    def test_parse_date_fail_3(self):
        date_str = "----"
        date = get_infos_bd.parse_date(date_str)
        self.assertEqual(date, date_str)


if __name__ == '__main__':
    unittest.main()
