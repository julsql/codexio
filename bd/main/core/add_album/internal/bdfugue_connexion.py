import platform
import random
import re

import cloudscraper
from bs4 import BeautifulSoup

from main.core.add_album.add_album_error import AddAlbumError
from main.core.add_album.bd_repository import BdRepository
from main.core.common.logger.logger import logger


class BdFugueRepository(BdRepository):

    def __init__(self) -> None:
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

    def __str__(self) -> str:
        return "BdFugueRepository"

    def get_infos(self, isbn: int) -> dict[str, str | float | int]:
        url = self.get_url(isbn)
        logger.info(url, extra={"isbn": isbn})
        html = self.get_html(url)
        soup = BeautifulSoup(html, 'html.parser')

        error_div = soup.find('title', string=re.compile(r'^Résultats de recherche pour :'))
        if error_div:
            raise AddAlbumError(f"{isbn} n'est pas dans BD Fugue ou bien il y a ambiguïté", isbn)

        infos = {}

        titles = soup.find_all("h1", {"class": [
            "order-1 mt-4 mb-3 lg:mb-4 lg:mt-0 text-2xl lg:text-5xl text-center lg:text-left w-full font-bold text-black lg:w-1/2 lg:pl-12 lg:float-right"]})
        if len(titles) > 0:
            title = titles[0].text
            parts = title.split("-", 1)

            if len(parts) == 2:
                series = parts[0].strip()
                album = parts[1].strip()
                infos["Série"] = series
                infos["Album"] = album
            else:
                # Si pas de "-", on considère que c'est le nom de l'album
                infos["Album"] = title.strip()

        # Recherche des divs contenant les informations
        divs = soup.find_all("div", {"class": ["col label w-1/3 product-attribute-label truncate",
                                               "col data w-2/3 product-attribute-value font-semibold"]})

        for i in range(0, len(divs), 2):
            label = divs[i].text.strip().split(":")[0].strip()
            value = divs[i + 1].text.strip()

            # Gestion des cas particuliers
            if label == "Auteur(s)":
                self._handle_authors(value, infos)
            elif label == "Format narratif" and value in ["Intégrale", "Histoires complètes"]:
                infos["Numéro"] = 1
            elif label in self.header.keys():
                self._handle_label(label, value, infos, isbn)

        # Remplir l'album avec la série si nécessaire
        if "Album" not in infos and "Série" in infos:
            infos["Album"] = infos["Série"]

        # Extraction du prix
        self._extract_price(soup, infos, isbn)

        # Extraction de l'image
        self._extract_image(soup, infos, isbn)

        # Extraction du synopsis
        self._extract_synopsis(soup, infos, isbn)

        # Extraction de la date
        self._parse_publication_date(infos, isbn)

        return infos

    def _handle_authors(self, value: str, infos: dict) -> None:
        """ Gérer le traitement des auteurs """
        personnes = value.split(" , ")
        for personne in personnes:
            match = re.search(r'^([\w\s-]+)\s+\(([^)]+)\)', personne.strip())
            if match:
                nom = match.group(1)
                attributs = [attr.strip() for attr in match.group(2).split(',')]
                for fonction in attributs:
                    if fonction in self.header.keys():
                        infos[fonction] = infos.get(fonction, '') + ("," if fonction in infos else "") + nom

    def _handle_label(self, label: str, value: str, infos: dict, isbn: int) -> None:
        """ Traiter les labels généraux """
        if self.header[label] == "Pages":
            try:
                infos[self.header[label]] = int(value)
            except ValueError:
                logger.warning("Pas de nombre de page correct trouvé", extra={"isbn": isbn})
        else:
            infos[self.header[label]] = value

    def _extract_price(self, soup: BeautifulSoup, infos: dict, isbn: int) -> None:
        """ Extraire le prix d'un album """
        price_meta = soup.find("meta", {"property": "product:price:amount"}) or soup.find("meta", {"itemprop": "price"})
        if price_meta:
            try:
                infos["Prix"] = float(price_meta.get("content"))
            except ValueError:
                logger.warning("Pas de prix correct trouvé", extra={"isbn": isbn})
        else:
            logger.warning("Pas de prix correct trouvé", extra={"isbn": isbn})

    def _extract_image(self, soup: BeautifulSoup, infos: dict, isbn: int) -> None:
        """ Extraire l'image de l'album """
        pattern = re.compile(r'https://www\.bdfugue\.com/media/catalog/product/cache/.*')
        image_element = soup.find('img', {'src': pattern})
        if image_element:
            infos["Image"] = image_element.get('src')
        else:
            logger.warning("Pas d'image trouvée", extra={"isbn": isbn})

    def _extract_synopsis(self, soup: BeautifulSoup, infos: dict, isbn: int) -> None:
        """ Extraire le synopsis de l'album """
        div_tag = soup.find("div", {"itemprop": "description"})
        if div_tag:
            infos["Synopsis"] = div_tag.get_text(strip=True)
        else:
            logger.warning("Pas de synopsis trouvé", extra={"isbn": isbn})

    def get_url(self, isbn: int) -> str:
        return f"https://www.bdfugue.com/catalogsearch/result/?q={isbn}"

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
            logger.error(f"Erreur lors de l'accès à {url}: {str(e)}")
            raise AddAlbumError(f"Impossible d'accéder à la page {url}")
