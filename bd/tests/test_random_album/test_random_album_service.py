import unittest
from datetime import date
from decimal import Decimal

from main.core.application.usecases.random_album.random_album_service import RandomAlbumService
from main.core.domain.model.album import Album
from tests.test_random_album.internal.random_album_in_memory import RandomAlbumInMemory


class TestRandomAlbumService(unittest.TestCase):
    def setUp(self) -> None:
        self.test_album = Album(
            isbn=123456789,
            title='Test Album',
            number='1',
            series='Test Series',
            writer='Test Writer',
            illustrator='Test Illustrator',
            publication_date=date(2024, 1, 1),
            purchase_price=Decimal("15.0"),
            number_of_pages=48,
            edition='Standard',
            synopsis='Test Synopsis',
            image='test.jpg'
        )

    def test_main_returns_none_when_no_album(self) -> None:
        # Arrange
        repository = RandomAlbumInMemory([Album(0)])
        service = RandomAlbumService(repository)

        # Act
        result = service.main()

        # Assert
        self.assertTrue(result.is_empty())
        self.assertTrue(repository.get_random_album_called)

    def test_main_returns_album_when_exists(self) -> None:
        # Arrange
        repository = RandomAlbumInMemory([self.test_album])
        service = RandomAlbumService(repository)

        # Act
        result = service.main()

        # Assert
        self.assertEqual(self.test_album, result)
        self.assertTrue(repository.get_random_album_called)
        self.assertEqual(self.test_album, result)


if __name__ == '__main__':
    unittest.main()
