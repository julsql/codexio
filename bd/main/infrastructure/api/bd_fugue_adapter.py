import platform
import random
import re
from decimal import Decimal

import cloudscraper
from bs4 import BeautifulSoup

from main.domain.exceptions.api_exceptions import ApiConnexionException, ApiConnexionDataNotFound
from main.domain.model.album import Album
from main.domain.ports.repositories.logger_repository import LoggerRepository
from main.infrastructure.api.base_album_adapter import BaseAlbumAdapter


class BdFugueAdapter(BaseAlbumAdapter):

    def __init__(self, logger_repository: LoggerRepository) -> None:
        super().__init__(logger_repository)
        self.header = {"Titre album": "Album", "Tome": "Numéro",
                       "Série": "Série", "Scénario": "Scénario",
                       "Dessin": "Dessin", "Couleurs": "Couleurs", "editeur": "Éditeur",
                       "date de parution": "Date de publication", "": "Édition",
                       "Nombre de pages": "Pages"}

        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15'
        ]
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

        titles = soup.find_all("h1", {"class": [
            "order-1 mt-4 mb-3 lg:mb-4 lg:mt-0 text-2xl lg:text-5xl text-center lg:text-left w-full font-bold text-black lg:w-1/2 lg:pl-12 lg:float-right"]})
        if len(titles) > 0:
            title = titles[0].text
            parts = title.split("-", 1)

            if len(parts) == 2:
                series = parts[0].strip()
                titre = parts[1].strip()
                album.serie = series
                album.title = titre
            else:
                # Si pas de "-", on considère que c'est le nom de l'album
                album.title = title.strip()

        # Recherche des divs contenant les informations
        divs = soup.find_all("div", {"class": ["col label w-1/3 product-attribute-label truncate",
                                               "col data w-2/3 product-attribute-value font-semibold"]})

        for i in range(0, len(divs), 2):
            label = divs[i].text.strip().split(":")[0].strip()
            value = divs[i + 1].text.strip()

            # Gestion des cas particuliers
            if label == "Auteur(s)":
                self._handle_authors(value, album)
            elif label == "Format narratif" and value in ["Intégrale", "Histoires complètes"]:
                album.numero = "1"
            elif label in self.header.keys():
                self._handle_labels(label, value, album)

        # Remplir l'album avec la série si nécessaire
        if album.title != "" and album.serie != "":
            album.title = album.serie

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
        personnes = value.split(" , ")
        for personne in personnes:
            match = re.search(r'^([\w\s-]+)\s+\(([^)]+)\)', personne.strip())
            if match:
                value = match.group(1)
                attributs = [attr.strip() for attr in match.group(2).split(',')]
                for fonction in attributs:
                    self._handle_label(fonction, value, album)
        return None

    def _handle_labels(self, label: str, value: str, album: Album) -> None:
        fonction = self.header[label]
        self._handle_label(fonction, value, album)

    def _handle_label(self, fonction: str, value: str, album: Album) -> None:
        """ Traiter les labels généraux """
        match fonction:
            case "Album":
                if value not in album.titre:
                    album.titre = album.titre + ("," if album.titre != "" else "") + value
            case "Numéro":
                if value not in album.numero:
                    album.numero = album.numero + ("," if album.numero != "" else "") + value
            case "Série":
                if value not in album.serie:
                    album.serie = album.serie + ("," if album.serie != "" else "") + value
            case "Scénario":
                if value not in album.scenariste:
                    album.scenariste = album.scenariste + ("," if album.scenariste != "" else "") + value
            case "Dessin":
                if value not in album.dessinateur:
                    album.dessinateur = album.dessinateur + ("," if album.dessinateur != "" else "") + value
            case "Couleurs":
                if value not in album.coloriste:
                    album.coloriste = album.coloriste + ("," if album.coloriste != "" else "") + value
            case "Éditeur":
                if value not in album.editeur:
                    album.editeur = album.editeur + ("," if album.editeur != "" else "") + value
            case "Date de publication":
                if value not in album.date_publication:
                    album.date_publication = self._parse_publication_date(value, self.isbn)
            case "Édition":
                if value not in album.edition:
                    album.edition = album.edition + ("," if album.edition != "" else "") + value
            case "Pages":
                if value not in album.nombre_pages:
                    album.nombre_pages = int(value)

    def _extract_price(self, soup: BeautifulSoup, album: Album) -> None:
        """ Extraire le prix d'un album """
        price_meta = soup.find("meta", {"property": "product:price:amount"}) or soup.find("meta", {"itemprop": "price"})
        if price_meta:
            try:
                album.prix = Decimal(price_meta.get("content"))
            except ValueError:
                self.logging_repository.warning("Pas de prix correct trouvé", extra={"isbn": self.isbn})
        else:
            self.logging_repository.warning("Pas de prix correct trouvé", extra={"isbn": self.isbn})

    def _extract_image(self, soup: BeautifulSoup, album: Album) -> None:
        """ Extraire l'image de l'album """
        pattern = re.compile(r'https://www\.bdfugue\.com/media/catalog/product/cache/.*')
        image_element = soup.find('img', {'src': pattern})
        if image_element:
            album.image_url = image_element.get('src')
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
        os_platform = 'windows'
        if platform.system().lower() == 'darwin':
            os_platform = 'darwin'
        elif platform.system().lower() == 'linux':
            os_platform = 'linux'

        scraper = cloudscraper.create_scraper(
            browser={'browser': 'chrome', 'platform': os_platform, 'desktop': True},
            delay=10
        )

        headers = {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'fr,fr-FR;q=0.8',
            'DNT': '1',
        }

        try:
            response = scraper.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            return response.text

        except Exception as e:
            self.logging_repository.error(f"Erreur lors de l'accès à {url}: {str(e)}")
            raise ApiConnexionException(f"Impossible d'accéder à la page {url}", str(self))
