import unittest
from unittest.mock import MagicMock, patch

from main.core.infrastructure.api.bd_google_adapter import BdGoogleAdapter
from main.core.infrastructure.api.book_adapter import BookAdapter
from main.core.infrastructure.api.internal.synopsis_picker_service import SynopsisPickerService
from tests.test_common.internal.logger_in_memory import LoggerInMemory

PETIT_PRINCE_ISBN = 9782070612758
FRENCH_SYNOPSIS = "Le premier soir je me suis donc endormi sur le sable à mille milles de toute terre habitée."
DUTCH_SYNOPSIS = ("Weemoedig-poëtisch sprookje waarin een prinsje van een andere planeet aan een piloot "
                  "over zijn ervaringen vertelt.")


def _google_item(volume_id: str, description: str) -> dict:
    return {
        "id": volume_id,
        "volumeInfo": {
            "title": "Le petit prince",
            "language": "fr",
            "description": description,
            "industryIdentifiers": [{"type": "ISBN_13", "identifier": str(PETIT_PRINCE_ISBN)}],
        },
    }


# Réponse réelle de Google Books : deux fiches « fr », la seconde avec un synopsis néerlandais
PETIT_PRINCE_RESPONSE = {
    "totalItems": 2,
    "items": [_google_item("NFWzngEACAAJ", FRENCH_SYNOPSIS), _google_item("SujnuQEACAAJ", DUTCH_SYNOPSIS)],
}


class TestSynopsisPickerService(unittest.TestCase):
    def test_prefers_french_synopsis(self) -> None:
        self.assertEqual(FRENCH_SYNOPSIS, SynopsisPickerService.pick([DUTCH_SYNOPSIS, FRENCH_SYNOPSIS]))

    def test_keeps_first_synopsis_on_tie(self) -> None:
        self.assertEqual("Premier", SynopsisPickerService.pick(["Premier", "Second"]))

    def test_ignores_empty_synopses(self) -> None:
        self.assertEqual(DUTCH_SYNOPSIS, SynopsisPickerService.pick(["", DUTCH_SYNOPSIS]))

    def test_returns_empty_without_synopsis(self) -> None:
        self.assertEqual("", SynopsisPickerService.pick([]))
        self.assertEqual("", SynopsisPickerService.pick(["", ""]))

    def test_french_score_of_foreign_text_is_zero(self) -> None:
        self.assertEqual(0.0, SynopsisPickerService.french_score(DUTCH_SYNOPSIS))


class TestGoogleAdaptersPickFrenchSynopsis(unittest.TestCase):
    def _get_synopsis(self, adapter_class, module: str) -> str:
        response = MagicMock(status_code=200)
        response.json.return_value = PETIT_PRINCE_RESPONSE
        with patch(f"{module}.requests.get", return_value=response):
            return adapter_class(LoggerInMemory()).get_infos(PETIT_PRINCE_ISBN).synopsis

    def test_bd_google_adapter_picks_french_synopsis(self) -> None:
        synopsis = self._get_synopsis(BdGoogleAdapter, "main.core.infrastructure.api.bd_google_adapter")
        self.assertEqual(FRENCH_SYNOPSIS, synopsis)

    def test_book_adapter_picks_french_synopsis(self) -> None:
        synopsis = self._get_synopsis(BookAdapter, "main.core.infrastructure.api.book_adapter")
        self.assertEqual(FRENCH_SYNOPSIS, synopsis)


if __name__ == '__main__':
    unittest.main()
