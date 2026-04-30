import re
from xml.etree import ElementTree as ET

import requests

from main.core.domain.exceptions.api_exceptions import ApiConnexionDataNotFound, ApiConnexionException
from main.core.domain.model.album import Album
from main.core.domain.ports.repositories.logger_repository import LoggerRepository
from main.core.infrastructure.api.base_album_adapter import BaseAlbumAdapter

NAMESPACES = {
    "srw": "http://www.loc.gov/zing/srw/",
    "oai_dc": "http://www.openarchives.org/OAI/2.0/oai_dc/",
    "dc": "http://purl.org/dc/elements/1.1/",
}

LANGUAGE_MAP = {"fre": "fr", "eng": "en", "ita": "it", "spa": "es", "ger": "de",
                "deu": "de", "por": "pt", "jpn": "ja", "rus": "ru", "ara": "ar",
                "chi": "zh", "zho": "zh", "lat": "la"}


class BnfAdapter(BaseAlbumAdapter):
    SRU_URL = "https://catalogue.bnf.fr/api/SRU"

    def __init__(self, logging_repository: LoggerRepository) -> None:
        super().__init__(logging_repository)

    def __str__(self) -> str:
        return "BnfAdapter"

    def get_infos(self, isbn: int) -> Album:
        isbn_query = self._isbn_for_query(isbn)
        params = {
            "version": "1.2",
            "operation": "searchRetrieve",
            "query": f'bib.isbn any "{isbn_query}"',
            "recordSchema": "dublincore",
            "maximumRecords": 1,
        }
        try:
            response = requests.get(self.SRU_URL, params=params, timeout=20)
        except requests.RequestException as e:
            raise ApiConnexionException(f"Erreur réseau BNF: {e}", str(self), isbn)
        if response.status_code != 200:
            raise ApiConnexionException(
                f"BNF a renvoyé {response.status_code}", str(self), isbn
            )

        try:
            root = ET.fromstring(response.text)
        except ET.ParseError as e:
            raise ApiConnexionException(f"Réponse BNF illisible: {e}", str(self), isbn)

        record = root.find(".//oai_dc:dc", NAMESPACES)
        if record is None:
            raise ApiConnexionDataNotFound(f"{isbn} introuvable à la BNF", str(self), isbn)
        # SRU peut renvoyer une notice qui ne correspond pas (matching fuzzy
        # sur EAN). On valide en extrayant les ISBN exacts ("ISBN …") de la
        # notice et en comparant à l'ISBN demandé sous ses deux formes.
        record_isbns = self._record_isbns(record)
        if isbn_query not in record_isbns and str(isbn) not in record_isbns:
            raise ApiConnexionDataNotFound(f"{isbn} introuvable à la BNF", str(self), isbn)

        book = Album(isbn=isbn)
        title_raw = self._dc(record, "title")
        book.title = self._extract_title(title_raw)
        book.writer = self._clean_person(self._dc(record, "creator"))
        book.translator = self._extract_translator(record)
        book.publisher = self._extract_publisher(self._dc(record, "publisher"))
        book.collection_book = self._extract_collection(self._dc(record, "description"))
        book.publication_date = self._parse_publication_date(self._dc(record, "date"), isbn)
        book.number_of_pages = self._extract_pages(self._dc(record, "format"))
        book.origin_language = LANGUAGE_MAP.get(self._dc(record, "language"), "")

        self.logging_repository.info(book.title, extra={"isbn": isbn})
        return book

    @staticmethod
    def _isbn_for_query(isbn: int) -> str:
        # La BNF n'indexe les ISBN que dans leur forme à 10 chiffres.
        s = str(isbn).replace("-", "").replace(" ", "")
        if len(s) == 13 and s.startswith("978"):
            nine = s[3:12]
            check = sum(int(d) * (i + 1) for i, d in enumerate(nine)) % 11
            return nine + ("X" if check == 10 else str(check))
        return s

    @staticmethod
    def _record_isbns(record) -> set[str]:
        isbns = set()
        for node in record.findall("dc:identifier", NAMESPACES):
            text = (node.text or "").strip()
            match = re.match(r"ISBN\s+([\dX-]+)", text, re.IGNORECASE)
            if match:
                isbns.add(match.group(1).replace("-", ""))
        return isbns

    @staticmethod
    def _dc(record, tag: str) -> str:
        node = record.find(f"dc:{tag}", NAMESPACES)
        if node is None or node.text is None:
            return ""
        return node.text.strip()

    @staticmethod
    def _extract_title(title_raw: str) -> str:
        if not title_raw:
            return ""
        # "Titre [: sous-titre] / auteurs ; mentions" → garder ce qui précède " / "
        title = title_raw.split(" / ", 1)[0].strip()
        return title

    @staticmethod
    def _clean_person(value: str) -> str:
        if not value:
            return ""
        # "Flaubert, Gustave (1821-1880). Auteur du texte" → "Gustave Flaubert"
        # On retire la mention finale ". Auteur ..." et les dates entre parenthèses.
        cleaned = re.sub(r"\.\s*Auteur[^.]*$", "", value).strip()
        cleaned = re.sub(r"\s*\(\d{4}-\d{0,4}\)\s*", " ", cleaned).strip()
        if "," in cleaned:
            last, first = cleaned.split(",", 1)
            cleaned = f"{first.strip()} {last.strip()}".strip()
        return cleaned

    def _extract_translator(self, record) -> str:
        names = []
        for contributor in record.findall("dc:contributor", NAMESPACES):
            text = (contributor.text or "").strip()
            if "Traducteur" in text:
                cleaned = self._clean_person(re.sub(r"\.\s*Traducteur[^.]*$", "", text))
                if cleaned:
                    names.append(cleaned)
        return ", ".join(names)

    @staticmethod
    def _extract_publisher(value: str) -> str:
        if not value:
            return ""
        # "Gallimard (Paris)" → "Gallimard"
        return re.sub(r"\s*\([^)]*\)\s*$", "", value).strip()

    @staticmethod
    def _extract_collection(description: str) -> str:
        if not description:
            return ""
        match = re.search(r"Collection\s*:\s*([^.;]+)", description)
        if not match:
            return ""
        return match.group(1).strip()

    @staticmethod
    def _extract_pages(format_str: str) -> int:
        if not format_str:
            return 0
        match = re.search(r"(\d+)\s*p\b", format_str)
        return int(match.group(1)) if match else 0
