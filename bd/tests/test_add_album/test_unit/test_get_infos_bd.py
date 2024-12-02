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

    def test_get_info_from_isbn_successfully(self):
        info = get_infos_bd.main(ASTERIX_ISBN)
        self.assertEqual(ASTERIX, info[0])

    def test_raise_error_get_info_from_incorrect_isbn(self):
        with self.assertRaises(error.Error):
            get_infos_bd.main("isbn incorrect")

    def test_raise_error_get_info_from_inexistant_isbn(self):
        _, result_error= get_infos_bd.main(self.INEXISTANT_ISBN)
        self.assertIsInstance(result_error, error.Error)


if __name__ == '__main__':
    unittest.main()
