import re
from decimal import Decimal

from bs4 import BeautifulSoup
from curl_cffi import requests as cffi_requests

from main.core.domain.exceptions.api_exceptions import ApiConnexionException, ApiConnexionDataNotFound
from main.core.domain.model.album import Album
from main.core.domain.ports.repositories.logger_repository import LoggerRepository
from main.core.infrastructure.api.base_album_adapter import BaseAlbumAdapter


class BdFugueAdapter(BaseAlbumAdapter):

    def __init__(self, logger_repository: LoggerRepository) -> None:
        super().__init__(logger_repository)
        self.header = {"Titre album": "Album", "Tome": "Numéro",
                       "Série": "Série", "Scénario": "Scénario",
                       "Dessin": "Dessin", "Couleurs": "Couleurs", "Éditeur": "Éditeur",
                       "date de parution": "Date de publication", "Édition": "Édition",
                       "Nombre de pages": "Pages"}
        self.isbn = 0

    def __str__(self) -> str:
        return "BdFugueRepository"

    def get_infos(self, isbn: int) -> Album:
        self.isbn = isbn
        url = self.get_url()
        self.logging_repository.info(url, extra={"isbn": isbn})
        html = self.get_html(url)
        soup = BeautifulSoup(html, 'html.parser')

        error_div = soup.find('title', string=re.compile(r'^Résultats de recherche pour :'))
        if error_div:
            raise ApiConnexionDataNotFound(f"{isbn} introuvable ou bien il y a ambiguïté", str(self), isbn)

        album = Album(isbn=isbn)

        titles = soup.find_all("h1", class_="font-bold")
        if len(titles) > 0:
            title = titles[0].text
            parts = title.split("-", 1)

            if len(parts) == 2:
                series = parts[0].strip()
                titre = parts[1].strip()
                album.series = series
                album.title = titre
            else:
                # Si pas de "-", on considère que c'est le nom de l'album
                album.title = title.strip()

        # Recherche des divs contenant les informations
        divs = soup.find_all(
            "div",
            class_=lambda c: c is not None and (
                "product-attribute-label" in c or "product-attribute-value" in c
            ),
        )

        for i in range(0, len(divs), 2):
            label = divs[i].text.strip().split(":")[0].strip()
            value = divs[i + 1].text.strip()

            # Gestion des cas particuliers
            if label == "Auteur(s)":
                self._handle_authors(value, album)
            elif label == "Format narratif" and value in ["Intégrale", "Histoires complètes"]:
                album.number = "1"
            elif label in self.header.keys():
                self._handle_labels(label, value, album)

        # Extraction du prix
        self._extract_price(soup, album)

        # Extraction de l'image
        self._extract_image(soup, album)

        # Extraction du synopsis
        self._extract_synopsis(soup, album)

        self.logging_repository.info(str(album), extra={"isbn": isbn})
        return album

    def _handle_authors(self, value: str, album: Album) -> None:
        """ Gérer le traitement des auteurs """
        for name, roles in re.findall(r'([^,()]+?)\s*\(([^)]+)\)', value):
            personne = name.strip()
            attributs = [attr.strip() for attr in roles.split(',')]
            for fonction in attributs:
                self._handle_label(fonction, personne, album)
        return None

    def _handle_labels(self, label: str, value: str, album: Album) -> None:
        fonction = self.header[label]
        self._handle_label(fonction, value, album)

    def _handle_label(self, fonction: str, value: str, album: Album) -> None:
        """ Traiter les labels généraux """
        match fonction:
            case "Album":
                album.title = value
            case "Numéro":
                album.number = value
            case "Série":
                album.series = value
            case "Scénario":
                if value not in album.writer:
                    album.writer = album.writer + ("," if album.writer != "" else "") + value
            case "Dessin":
                if value not in album.illustrator:
                    album.illustrator = album.illustrator + ("," if album.illustrator != "" else "") + value
            case "Couleurs":
                if value not in album.colorist:
                    album.colorist = album.colorist + ("," if album.colorist != "" else "") + value
            case "Éditeur":
                album.publisher = value
            case "Date de publication":
                if album.publication_date is None:
                    album.publication_date = self._parse_publication_date(value, self.isbn)
            case "Édition":
                if value not in album.edition:
                    album.edition = album.edition + ("," if album.edition != "" else "") + value
            case "Pages":
                if album.number_of_pages == 0:
                    try:
                        album.number_of_pages = int(value)
                    except ValueError:
                        self.logging_repository.warning(
                            f"{value} est un nombre de pages incorrect", extra={"isbn": self.isbn}
                        )

    def _extract_price(self, soup: BeautifulSoup, album: Album) -> None:
        """ Extraire le prix d'un album """
        price_meta = soup.find("meta", {"property": "product:price:amount"}) or soup.find("meta", {"itemprop": "price"})
        if price_meta:
            try:
                album.purchase_price = Decimal(price_meta.get("content"))
            except ValueError:
                self.logging_repository.warning("Pas de prix correct trouvé", extra={"isbn": self.isbn})
        else:
            self.logging_repository.warning("Pas de prix correct trouvé", extra={"isbn": self.isbn})

    def _extract_image(self, soup: BeautifulSoup, album: Album) -> None:
        """ Extraire l'image de l'album """
        pattern = re.compile(r'https://www\.bdfugue\.com/media/catalog/product/cache/.*')
        image_element = soup.find('img', {'src': pattern})
        if image_element:
            album.image = image_element.get('src')
        else:
            self.logging_repository.warning("Pas d'image trouvée", extra={"isbn": self.isbn})

    def _extract_synopsis(self, soup: BeautifulSoup, album: Album) -> None:
        """ Extraire le synopsis de l'album """
        div_tag = soup.find("div", {"itemprop": "description"})
        if div_tag:
            album.synopsis = div_tag.get_text(strip=True)
        else:
            self.logging_repository.warning("Pas de synopsis trouvé", extra={"isbn": self.isbn})

    def get_url(self) -> str:
        return f"https://www.bdfugue.com/catalogsearch/result/?q={self.isbn}"

    def get_html(self, url: str) -> str:
        try:
            response = cffi_requests.get(url, impersonate="chrome131", timeout=30)
            response.raise_for_status()
            return response.text

        except Exception as e:
            self.logging_repository.error(f"Erreur lors de l'accès à {url}: {str(e)}")
            raise ApiConnexionException(f"Impossible d'accéder à la page {url}", str(self))
