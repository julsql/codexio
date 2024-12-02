import datetime
import unittest

from main.add_album import error
from main.add_album import get_infos_bd
from tests.test_add_album.data.album_data_set import ASTERIX_ISBN, ASTERIX_LINK, ASTERIX


class TestGetInfosBd(unittest.TestCase):

    INEXISTANT_ISBN = 9791038203907

    def test_correct_get_link(self):
        link = get_infos_bd.get_link(ASTERIX_ISBN)
        self.assertEqual(ASTERIX_LINK, link)

    def test_dont_get_link(self):
        link = get_infos_bd.get_link("")
        self.assertEqual(0, link)

    def test_get_correct_info_successfully(self):
        info = get_infos_bd.corriger_info({}, "")
        self.assertEqual({
            'Album': '', 'Couleurs': '', 'Date de publication': '',
            'Dessin': '', 'Édition': '', 'ISBN': '', 'Image': '',
            'Numéro': '', 'Pages': '', 'Prix': '', 'Scénario': '',
            'Synopsis': '', 'Série': '', 'Éditeur': ''},
            info)

    def test_raise_error_correct_empty_value(self):
        with self.assertRaises(AttributeError):
            get_infos_bd.corriger_info("", "")

    def test_get_info_from_isbn_successfully(self):
        info = get_infos_bd.main(ASTERIX_ISBN)
        self.assertEqual(ASTERIX, info[0])

    def test_raise_error_get_info_from_incorrect_isbn(self):
        with self.assertRaises(error.Error):
            get_infos_bd.main("isbn incorrect")

    def test_raise_error_get_info_from_inexistant_isbn(self):
        _, result_error= get_infos_bd.main(self.INEXISTANT_ISBN)
        self.assertIsInstance(result_error, error.Error)

    def test_parse_date_pass_1(self):
        date = get_infos_bd.parse_date("2021")
        self.assertEqual(datetime.date(2021, 1, 1).strftime("%Y-%m-%d"),
                         date)

    def test_parse_date_pass_2(self):
        date = get_infos_bd.parse_date("3 FEVRIER 2021")
        self.assertEqual(datetime.date(2021, 2, 3).strftime("%Y-%m-%d"),
                         date)

    def test_parse_date_pass_3(self):
        date = get_infos_bd.parse_date("3 FÉVRIER 2021")
        self.assertEqual(datetime.date(2021, 2, 3).strftime("%Y-%m-%d"),
                         date)

    def test_parse_date_pass_4(self):
        date = get_infos_bd.parse_date("aout 2021")
        self.assertEqual(datetime.date(2021, 8, 1).strftime("%Y-%m-%d"),
                         date)

    def test_parse_date_pass_5(self):
        date = get_infos_bd.parse_date("4th March 2021")
        self.assertEqual(datetime.date(2021, 3, 4).strftime("%Y-%m-%d"),
                         date)

    def test_parse_date_pass_6(self):
        date = get_infos_bd.parse_date("April, 2nd 2021")
        self.assertEqual(datetime.date(2021, 4, 2).strftime("%Y-%m-%d"),
                         date)

    def test_parse_date_pass_7(self):
        date = get_infos_bd.parse_date("février 2021")
        self.assertEqual(datetime.date(2021, 2, 1).strftime("%Y-%m-%d"),
                         date)

    def test_parse_date_pass_8(self):
        date = get_infos_bd.parse_date("2021 Septembre 4e")
        self.assertEqual(datetime.date(2021, 9, 4).strftime("%Y-%m-%d"),
                         date)

    def test_parse_date_pass_9(self):
        date = get_infos_bd.parse_date("13/11/2021")
        self.assertEqual(datetime.date(2021, 11, 13).strftime("%Y-%m-%d"),
                         date)

    def test_parse_date_pass_10(self):
        date = get_infos_bd.parse_date("2021/04/30")
        self.assertEqual(datetime.date(2021, 4, 30).strftime("%Y-%m-%d"),
                         date)

    def test_parse_date_pass_11(self):
        date = get_infos_bd.parse_date("10 02 2021")
        self.assertEqual(datetime.date(2021, 2, 10).strftime("%Y-%m-%d"),
                         date)

    def test_parse_date_fail_1(self):
        date_str = "BRUH"
        date = get_infos_bd.parse_date(date_str)
        self.assertEqual(date_str, date)

    def test_parse_date_fail_2(self):
        date_str = ""
        date = get_infos_bd.parse_date(date_str)
        self.assertEqual(date_str, date)

    def test_parse_date_fail_3(self):
        date_str = "----"
        date = get_infos_bd.parse_date(date_str)
        self.assertEqual(date_str, date)


if __name__ == '__main__':
    unittest.main()
