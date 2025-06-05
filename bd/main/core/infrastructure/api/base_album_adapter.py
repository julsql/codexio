from abc import ABC
from datetime import date
from typing import Optional

from main.core.domain.ports.repositories.album_repository import AlbumRepository
from main.core.domain.ports.repositories.logger_repository import LoggerRepository
from main.core.infrastructure.api.internal.date_parser_service import DateParserService


class BaseAlbumAdapter(AlbumRepository, ABC):
    def __init__(self, logging_repository: LoggerRepository):
        self.logging_repository = logging_repository

    def _parse_publication_date(self, date_string: str, isbn: int) -> Optional[date]:
        if date_string:
            parsed_date = DateParserService.parse_date(date_string)
            if parsed_date:
                return parsed_date
            else:
                self.logging_repository.warning(
                    f"Problème de parsing de la date: {date_string}",
                    isbn=isbn
                )
        return None
