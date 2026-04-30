import random
import re
import string
import time
from decimal import Decimal

from bs4 import BeautifulSoup
from curl_cffi import requests as cffi_requests

from main.core.domain.exceptions.api_exceptions import ApiConnexionException, ApiConnexionDataNotFound
from main.core.domain.model.album import Album
from main.core.domain.ports.repositories.logger_repository import LoggerRepository
from main.core.infrastructure.api.base_album_adapter import BaseAlbumAdapter


_BASE36 = string.digits + string.ascii_lowercase


def _base36(n: int) -> str:
    if n == 0:
        return "0"
    out = ""
    while n:
        n, r = divmod(n, 36)
        out = _BASE36[r] + out
    return out


class BdPhileAdapter(BaseAlbumAdapter):
    def __init__(self, logger_repository: LoggerRepository) -> None:
        super().__init__(logger_repository)
        self.isbn = 0
        self._session = None

    def _get_session(self):
        # Le serveur exige un cookie js_token (posé en JS dans main.js,
        # format "<ts_b36>.<random_b36>", max-age 5 min) sinon /search/ renvoie "Oups".
        if self._session is None:
            self._session = cffi_requests.Session(impersonate="chrome131")
        ts = _base36(int(time.time()))
        rand = "".join(random.choices(_BASE36, k=8))
        self._session.cookies.set(
            "js_token", f"{ts}.{rand}", domain="www.bdphile.fr", path="/"
        )
        return self._session

    def __str__(self) -> str:
        return "BdPhileRepository"

    def get_infos(self, isbn: int) -> Album:
        self.isbn = isbn
        album = Album(isbn=isbn)
        url = self.get_url()
        html = self.get_html(url)
        soup = BeautifulSoup(html, 'html.parser')

        # Extraction du titre
        self._extract_title(soup, album)

        # Extraction des informations supplémentaires
        self._extract_additional_info(soup, album)

        # Image
        self._extract_image(soup, album)

        # Synopsis
        self._extract_synopsis(soup, album)

        self.logging_repository.info(str(album), extra={"isbn": isbn})
        return album

    def _extract_title(self, soup: BeautifulSoup, album: Album) -> None:
        """ Extraire les informations du titre """
        album_tag = soup.find("section", id="page-title")
        if not album_tag:
            self.logging_repository.warning("Informations sur le titre non trouvées", extra={"isbn": self.isbn})
            return None

        series_tag = album_tag.find("h1")
        if not series_tag:
            self.logging_repository.warning("Informations sur la série non trouvées", extra={"isbn": self.isbn})

        else:
            series = series_tag.get_text()
            series = series.strip().split("\n")[0]
            album.series = series
        title_tag = album_tag.find("h2")
        if not title_tag:
            self.logging_repository.warning("Informations sur le titre non trouvées", extra={"isbn": self.isbn})
        else:
            title = title_tag.get_text()
            match = re.search(r"^Tome\s+(\d+)\s*:", title, re.IGNORECASE)

            if match:
                numero = match.group(1)
                titre = title[match.end():].strip()
                album.number = numero
                album.title = titre
            else:
                # Pas de numéro de tome trouvé
                self.logging_repository.debug(
                    f"Pas de numéro de tome trouvé dans le titre: '{title}'",
                    extra={"isbn": self.isbn}
                )
                album.title = title.strip()
        return None

    def _extract_additional_info(self, soup: BeautifulSoup, album: Album) -> None:
        """ Extraire les informations supplémentaires """
        keys = ['Scénario', 'Dessin', 'Couleurs', 'Éditeur', 'Date de publication', 'Édition', 'Format']
        current_key = ""
        album_format = ""
        book_info = soup.find('div', id='book-info')
        for tag in book_info.find_all(['dt', 'dd']):
            if tag.name == 'dt':
                current_key = tag.get_text(strip=True)
                if album.contains(current_key):
                    current_key = None
            elif tag.name == 'dd' and current_key in keys:
                dd_text = " ".join(tag.stripped_strings)
                match current_key:
                    case "Scénario":
                        album.writer = album.writer + ("," if album.writer != "" else "") + dd_text
                    case "Dessin":
                        album.illustrator = album.illustrator + ("," if album.illustrator != "" else "") + dd_text
                    case "Couleurs":
                        album.colorist = album.colorist + ("," if album.colorist != "" else "") + dd_text
                    case "Éditeur":
                        album.publisher = album.publisher + ("," if album.publisher != "" else "") + dd_text
                    case "Date de publication":
                        album.publication_date = self._parse_publication_date(dd_text, self.isbn)
                    case "Édition":
                        if dd_text not in album.edition:
                            album.edition = album.edition + ("," if album.edition != "" else "") + dd_text
                    case "Format":
                        album_format = dd_text
        self._handle_format(album, album_format)

    def _handle_format(self, album: Album, album_format: str) -> None:
        """ Extraire le format et le prix """
        if album_format:
            for value in album_format.split("-"):
                if "pages" in value:
                    self._extract_pages(value, album)
                elif "€" in value:
                    self._extract_price(value, album)

    def _extract_pages(self, value: str, album: Album) -> None:
        """ Extraire le nombre de planches """
        try:
            album.number_of_pages = int(value.replace("pages", "").strip())
        except ValueError:
            self.logging_repository.warning(f"{value} est un nombre de planches incorrect", extra={"isbn": self.isbn})

    def _extract_price(self, value: str, album: Album) -> None:
        """ Extraire le prix """
        try:
            album.purchase_price = Decimal(value.replace("€", "").strip())
        except ValueError:
            self.logging_repository.warning(f"{value} est un prix incorrect", extra={"isbn": self.isbn})

    def _extract_image(self, soup: BeautifulSoup, album: Album) -> None:
        """ Extraire l'image """
        meta_tag = soup.find('meta', attrs={'property': 'og:image'})
        if not meta_tag:
            self.logging_repository.warning("Image non trouvée", extra={"isbn": self.isbn})
            return
        album.image = meta_tag['content']

    def _extract_synopsis(self, soup: BeautifulSoup, album: Album) -> None:
        """ Extraire le synopsis """
        synopsis_tag = soup.find('p', class_='synopsis')
        if not synopsis_tag:
            self.logging_repository.warning("Synopsis non trouvé", extra={"isbn": self.isbn})
            return

        cleaned_synopsis = (''.join(str(tag) for tag in synopsis_tag.decode_contents())
                            .strip()
                            .replace('\r', '')
                            .replace('\n', '')
                            .replace('\t', ''))
        if 'Le synopsis de cet album est manquant' in cleaned_synopsis:
            self.logging_repository.warning("Synopsis manquant", extra={"isbn": self.isbn})
            return
        album.synopsis = cleaned_synopsis

    def get_url(self) -> str:
        """Trouver lien BD bdphile.fr à partir de son ISBN"""

        search_link = "https://www.bdphile.fr/search/album/?q={}".format(self.isbn)
        try:
            response = self._get_session().get(
                search_link, timeout=30, headers={"Referer": "https://www.bdphile.fr/"}
            )
            response.raise_for_status()
        except Exception as e:
            self.logging_repository.error(f"La requête a échoué pour {search_link}: {e}")
            raise ApiConnexionException(
                f"Impossible d'afficher le code html de la page {search_link}", str(self)
            )

        # Une recherche sans résultat (ex. ISBN 0) renvoie un 302 vers la home.
        if "/search/" not in str(response.url):
            raise ApiConnexionDataNotFound(f"ISBN {self.isbn} introuvable", str(self), self.isbn)

        soup = BeautifulSoup(response.text, "html.parser")
        if soup.find("title", string=re.compile(r"^Oups")):
            raise ApiConnexionDataNotFound(
                f"ISBN {self.isbn} introuvable (cookie js_token rejeté ?)",
                str(self),
                self.isbn,
            )
        a_tag = soup.find(
            "a",
            href=lambda href: href
            and re.match(r"^https://www\.bdphile\.fr/album/(view/\d+/|bd/\d+-)", href),
        )
        if a_tag:
            return a_tag.get("href")
        raise ApiConnexionDataNotFound(f"ISBN {self.isbn} introuvable", str(self), self.isbn)

    def get_html(self, url: str) -> str:
        try:
            response = self._get_session().get(url, timeout=30)
            response.raise_for_status()
            return response.text
        except Exception as e:
            self.logging_repository.error(f"La requête a échoué pour {url}: {e}")
            raise ApiConnexionException(f"Impossible d'afficher le code html de la page {url}", str(self))
