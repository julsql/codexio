from abc import ABC
from datetime import date
from typing import Optional

import requests

from config.settings import GOOGLE_KEY
from main.core.domain.exceptions.api_exceptions import ApiConnexionDataNotFound, ApiConnexionException
from main.core.domain.model.album import Album
from main.core.domain.ports.repositories.add_album_repository import AddAlbumRepository
from main.core.domain.ports.repositories.logger_repository import LoggerRepository
from main.core.infrastructure.api.internal.date_parser_service import DateParserService


class BookAdapter(AddAlbumRepository, ABC):
    def __init__(self, logging_repository: LoggerRepository):
        self.logging_repository = logging_repository
        self.api_url = "https://www.googleapis.com/books/v1/volumes"

    def __str__(self) -> str:
        return "BookAdapter"

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

    def _get_best_cover_image(self, volume_info: dict) -> str:
        image_links = volume_info.get("imageLinks", {})
        for key in ["extraLarge", "large", "medium", "small", "thumbnail", "smallThumbnail"]:
            if key in image_links:
                return image_links[key]
        return ""

    def _parse_google_publication_date(self, date_string: str, isbn: int) -> Optional[date]:
        if date_string:
            parsed_date = DateParserService.parse_google_date(date_string)
            if parsed_date:
                return parsed_date
            else:
                self.logging_repository.warning(
                    f"Problème de parsing de la date: {date_string}",
                    isbn=isbn
                )
        return None

    def get_infos(self, isbn: int) -> Album:
        book = Album(isbn=isbn)

        params = {
            "q": f"isbn:{isbn}",
            "key": GOOGLE_KEY
        }

        response = requests.get(self.api_url, params=params)
        if response.status_code != 200:
            raise ApiConnexionException(f"{response.text}: Erreur lors de l'appel à l'API Google Books", str(self), isbn)

        data = response.json()
        if "items" not in data:
            raise ApiConnexionDataNotFound(f"{isbn} introuvable", str(self), isbn)

        volume = data["items"][0]["volumeInfo"]

        book.title = volume.get("title", "")
        self.logging_repository.info(book.title, extra={"isbn": isbn})
        book.writer = ", ".join(volume.get("authors", []))
        book.publisher = volume.get("publisher", "")
        book.publication_date = self._parse_google_publication_date(volume.get("publishedDate"), isbn)
        book.number_of_pages = volume.get("pageCount", 0)
        book.literary_genre = ", ".join(volume.get("categories", []))
        book.origin_language = volume.get("language", "")
        book.image = self._get_best_cover_image(volume)
        book.synopsis = volume.get("description", "")
        return book
