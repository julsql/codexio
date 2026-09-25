from datetime import date, timedelta
from decimal import Decimal
from typing import Optional

from django.utils import timezone

from main.core.domain.model.album import Album
from main.core.domain.ports.repositories.album_cache_repository import AlbumCacheRepository
from main.core.domain.ports.repositories.logger_repository import LoggerRepository
from main.core.infrastructure.persistence.database.models import AlbumInfosCache

DATE_FIELDS = ("publication_date",)
DECIMAL_FIELDS = ("purchase_price",)


class AlbumCacheAdapter(AlbumCacheRepository):
    def __init__(self, logging_repository: LoggerRepository, ttl_days: int) -> None:
        self.logging_repository = logging_repository
        self.ttl_days = ttl_days

    def get(self, source: str, isbn: int) -> Optional[Album]:
        if self.ttl_days <= 0:
            return None

        try:
            entry = AlbumInfosCache.objects.filter(source=source, isbn=isbn).first()
        except Exception as e:
            # Un cache indisponible ne doit jamais empêcher d'interroger la source
            self.logging_repository.error(f"Lecture du cache impossible pour {source}: {str(e)}")
            return None

        if entry is None:
            return None

        if entry.fetched_at < timezone.now() - timedelta(days=self.ttl_days):
            self.logging_repository.info(f"Notice périmée pour {source}", isbn=isbn)
            return None

        return self._to_album(entry.payload, isbn)

    def save(self, source: str, isbn: int, album: Album) -> None:
        if self.ttl_days <= 0:
            return

        try:
            AlbumInfosCache.objects.update_or_create(
                source=source,
                isbn=isbn,
                defaults={"payload": self._to_payload(album)},
            )
        except Exception as e:
            # Idem : échouer à mémoriser ne doit pas faire échouer la requête
            self.logging_repository.error(f"Écriture du cache impossible pour {source}: {str(e)}")

    @staticmethod
    def _to_payload(album: Album) -> dict:
        payload = {}
        for field, value in vars(album).items():
            if isinstance(value, date):
                payload[field] = value.isoformat()
            elif isinstance(value, Decimal):
                payload[field] = str(value)
            else:
                payload[field] = value
        return payload

    @staticmethod
    def _to_album(payload: dict, isbn: int) -> Album:
        values = dict(payload)
        values["isbn"] = isbn

        for field in DATE_FIELDS:
            if values.get(field):
                values[field] = date.fromisoformat(values[field])
        for field in DECIMAL_FIELDS:
            if values.get(field) is not None:
                values[field] = Decimal(str(values[field]))

        known = {f for f in vars(Album(isbn=0))}
        return Album(**{k: v for k, v in values.items() if k in known})
