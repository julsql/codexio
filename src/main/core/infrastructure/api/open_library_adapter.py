import requests

from main.core.domain.exceptions.api_exceptions import ApiConnexionDataNotFound, ApiConnexionException
from main.core.domain.model.album import Album
from main.core.domain.ports.repositories.logger_repository import LoggerRepository
from main.core.infrastructure.api.base_album_adapter import BaseAlbumAdapter

LANGUAGE_MAP = {"fre": "fr", "eng": "en", "ita": "it", "spa": "es", "ger": "de",
                "deu": "de", "por": "pt", "jpn": "ja", "rus": "ru", "ara": "ar",
                "chi": "zh", "zho": "zh", "lat": "la"}

TRANSLATOR_MARKERS = ("trad.", "traduit", "traduction")


class OpenLibraryAdapter(BaseAlbumAdapter):
    BASE_URL = "https://openlibrary.org"
    COVER_URL = "https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"

    def __init__(self, logging_repository: LoggerRepository) -> None:
        super().__init__(logging_repository)

    def __str__(self) -> str:
        return "OpenLibraryAdapter"

    def get_infos(self, isbn: int) -> Album:
        edition = self._fetch_json(f"{self.BASE_URL}/isbn/{isbn}.json", isbn)

        book = Album(isbn=isbn)
        book.title = self._compose_title(edition)
        book.publisher = self._first(edition.get("publishers"))
        book.collection_book = self._first(edition.get("series"))
        book.publication_date = self._parse_publication_date(edition.get("publish_date"), isbn)
        book.number_of_pages = edition.get("number_of_pages") or 0
        book.origin_language = self._extract_language(edition.get("languages"))
        book.image = self._extract_cover(edition.get("covers"))

        contributions = edition.get("contributions") or []
        work = self._fetch_work(edition.get("works"), isbn)
        author_entries = edition.get("authors") or (work.get("authors") if work else None) or []
        authors = self._extract_authors(author_entries, isbn)
        book.writer = self._merge_people(authors, [c for c in contributions if not self._is_translator(c)])
        book.translator = ", ".join(c for c in contributions if self._is_translator(c)) or ""

        if work:
            book.synopsis = self._extract_description(work.get("description"))
            if not book.collection_book:
                book.collection_book = self._first(work.get("series"))
            book.literary_genre = self._extract_genre(work.get("subjects"))

        self.logging_repository.info(book.title, extra={"isbn": isbn})
        return book

    def _fetch_json(self, url: str, isbn: int) -> dict:
        try:
            response = requests.get(url, timeout=20, headers={"User-Agent": "codexio/1.0"})
        except requests.RequestException as e:
            raise ApiConnexionException(f"Erreur réseau OpenLibrary: {e}", str(self), isbn)
        if response.status_code == 404:
            raise ApiConnexionDataNotFound(f"{isbn} introuvable sur OpenLibrary", str(self), isbn)
        if response.status_code != 200:
            raise ApiConnexionException(
                f"OpenLibrary a renvoyé {response.status_code}", str(self), isbn
            )
        try:
            return response.json()
        except ValueError as e:
            raise ApiConnexionException(f"Réponse OpenLibrary illisible: {e}", str(self), isbn)

    def _fetch_work(self, works: list | None, isbn: int) -> dict | None:
        if not works:
            return None
        key = works[0].get("key")
        if not key:
            return None
        try:
            return self._fetch_json(f"{self.BASE_URL}{key}.json", isbn)
        except (ApiConnexionException, ApiConnexionDataNotFound) as e:
            self.logging_repository.warning(f"Œuvre OpenLibrary inaccessible: {e}", extra={"isbn": isbn})
            return None

    def _extract_authors(self, authors: list, isbn: int) -> list[str]:
        names = []
        for entry in authors:
            key = entry.get("key") or (entry.get("author") or {}).get("key")
            if not key:
                continue
            try:
                data = self._fetch_json(f"{self.BASE_URL}{key}.json", isbn)
            except (ApiConnexionException, ApiConnexionDataNotFound):
                continue
            name = data.get("name") or data.get("personal_name")
            if name:
                names.append(name)
        return names

    @staticmethod
    def _compose_title(edition: dict) -> str:
        title = (edition.get("title") or "").strip()
        subtitle = (edition.get("subtitle") or "").strip()
        if title and subtitle:
            return f"{title} : {subtitle}"
        return title

    @staticmethod
    def _merge_people(primary: list[str], secondary: list[str]) -> str:
        seen = []
        for name in primary + secondary:
            cleaned = (name or "").strip().rstrip(".").strip()
            if cleaned and cleaned not in seen:
                seen.append(cleaned)
        return ", ".join(seen)

    @staticmethod
    def _is_translator(contribution: str) -> bool:
        lowered = (contribution or "").lower()
        return any(marker in lowered for marker in TRANSLATOR_MARKERS)

    @staticmethod
    def _first(values: list | None) -> str:
        if not values:
            return ""
        return str(values[0]).strip()

    @staticmethod
    def _extract_language(languages: list | None) -> str:
        if not languages:
            return ""
        key = languages[0].get("key", "")
        code = key.rsplit("/", 1)[-1]
        return LANGUAGE_MAP.get(code, code)

    @classmethod
    def _extract_cover(cls, covers: list | None) -> str:
        if not covers:
            return ""
        return cls.COVER_URL.format(cover_id=covers[0])

    @staticmethod
    def _extract_description(description) -> str:
        if isinstance(description, dict):
            description = description.get("value", "")
        text = (description or "").strip()
        # OpenLibrary glisse parfois après une ligne "----------" des liens
        # externes ("See also", footnotes markdown). On garde uniquement la
        # première section narrative.
        return text.split("----------", 1)[0].strip()

    @staticmethod
    def _extract_genre(subjects: list | None) -> str:
        if not subjects:
            return ""
        # Garder les premiers sujets courts et significatifs
        keep = []
        for subj in subjects:
            cleaned = subj.strip()
            if not cleaned or len(cleaned) > 40:
                continue
            keep.append(cleaned)
            if len(keep) >= 3:
                break
        return ", ".join(keep)
