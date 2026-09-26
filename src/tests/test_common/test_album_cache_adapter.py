import os
import sys
from datetime import date, timedelta
from decimal import Decimal

import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.test import TestCase
from django.utils import timezone

from main.core.domain.model.album import Album
from main.core.infrastructure.persistence.database.album_cache_adapter import AlbumCacheAdapter
from main.core.infrastructure.persistence.database.models import AlbumInfosCache
from tests.test_common.internal.logger_in_memory import LoggerInMemory

ISBN = 9782864976165


class TestAlbumCacheAdapter(TestCase):
    def setUp(self):
        self.logger = LoggerInMemory()
        self.adapter = AlbumCacheAdapter(self.logger, ttl_days=30)

    def _album(self) -> Album:
        return Album(
            isbn=ISBN,
            title="L'empire du milieu",
            series="Astérix",
            publication_date=date(2023, 2, 8),
            number_of_pages=48,
            purchase_price=Decimal("10.5"),
            synopsis="Nous sommes en 50 av J.-C.",
        )

    def test_returns_nothing_when_never_stored(self):
        self.assertIsNone(self.adapter.get("bdphile", ISBN))

    def test_round_trip_keeps_date_and_decimal_types(self):
        self.adapter.save("bdphile", ISBN, self._album())

        restored = self.adapter.get("bdphile", ISBN)

        self.assertEqual("L'empire du milieu", restored.title)
        self.assertEqual(date(2023, 2, 8), restored.publication_date)
        self.assertEqual(Decimal("10.5"), restored.purchase_price)
        self.assertEqual(48, restored.number_of_pages)
        self.assertEqual(ISBN, restored.isbn)

    def test_empty_optional_fields_survive(self):
        self.adapter.save("bdphile", ISBN, Album(isbn=ISBN, title="Sans date"))

        restored = self.adapter.get("bdphile", ISBN)

        self.assertIsNone(restored.publication_date)
        self.assertIsNone(restored.purchase_price)
        self.assertEqual("", restored.series)

    def test_entries_are_isolated_per_source(self):
        self.adapter.save("bdphile", ISBN, self._album())

        self.assertIsNone(self.adapter.get("bdgest", ISBN))

    def test_saving_twice_updates_instead_of_duplicating(self):
        self.adapter.save("bdphile", ISBN, self._album())
        updated = self._album()
        updated.title = "Titre corrigé"
        self.adapter.save("bdphile", ISBN, updated)

        self.assertEqual(1, AlbumInfosCache.objects.filter(source="bdphile", isbn=ISBN).count())
        self.assertEqual("Titre corrigé", self.adapter.get("bdphile", ISBN).title)

    def test_an_expired_entry_is_ignored(self):
        self.adapter.save("bdphile", ISBN, self._album())
        AlbumInfosCache.objects.filter(source="bdphile", isbn=ISBN).update(
            fetched_at=timezone.now() - timedelta(days=31)
        )

        self.assertIsNone(self.adapter.get("bdphile", ISBN))

    def test_a_ttl_of_zero_disables_the_cache(self):
        disabled = AlbumCacheAdapter(self.logger, ttl_days=0)

        disabled.save("bdphile", ISBN, self._album())

        self.assertEqual(0, AlbumInfosCache.objects.count())
        self.assertIsNone(disabled.get("bdphile", ISBN))
