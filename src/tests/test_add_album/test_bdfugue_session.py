import unittest
from unittest.mock import MagicMock, patch

from main.core.infrastructure.api.bd_fugue_adapter import BdFugueAdapter
from tests.test_common.internal.logger_in_memory import LoggerInMemory


class TestBdFugueSession(unittest.TestCase):
    """Les cookies Cloudflare vivent dans la session : elle doit être réutilisée d'une requête à l'autre."""

    @patch("main.core.infrastructure.api.bd_fugue_adapter.cffi_requests.Session")
    def test_reuses_the_same_session_across_requests(self, session_class: MagicMock) -> None:
        session_class.return_value.get.return_value = MagicMock(status_code=200, text="<html></html>")
        adapter = BdFugueAdapter(LoggerInMemory())

        adapter.get_html("https://www.bdfugue.com/a")
        adapter.get_html("https://www.bdfugue.com/b")

        session_class.assert_called_once_with(impersonate="chrome131")
        self.assertEqual(2, session_class.return_value.get.call_count)


if __name__ == '__main__':
    unittest.main()
