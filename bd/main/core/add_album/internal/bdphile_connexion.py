import datetime

import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse, ParserError

from main.core.add_album.add_album_error import AddAlbumError
from main.core.add_album.bd_repository import BdRepository
from main.core.common.logger.logger import logger


class BdPhileRepository(BdRepository):

    def __str__(self) -> str:
        return "BdPhileRepository"

    def get_infos(self, isbn: int) -> dict[str, str | float | int]:
        informations = {}
        url = self.get_url(isbn)
        html = self.get_html(url)
        soup = BeautifulSoup(html, 'html.parser')

        # Extraction du titre
        self._extract_title(soup, informations)

        # Extraction des informations supplémentaires
        self._extract_additional_info(soup, informations)

        # Format et prix
        self._extract_format_and_price(informations, isbn)

        # Image
        self._extract_image(soup, informations)

        # Synopsis
        self._extract_synopsis(soup, informations)

        # Date de publication
        self._parse_publication_date(informations, isbn)

        logger.info(informations, extra={"isbn": isbn})
        return informations

    def _extract_title(self, soup: BeautifulSoup, informations: dict) -> None:
        """ Extraire les informations du titre """
        title_tag = soup.find('title')
        if title_tag:
            title_text = title_tag.get_text().split("|")[0].strip()
            elements = title_text.split(" - ")
            informations["Série"] = elements[0].strip()
            if len(elements) > 1:
                serie = elements[1].split(".")
                if serie[0] == "One-shot":
                    informations["Numéro"] = 1
                    informations["Album"] = informations["Série"]
                elif len(serie) > 1:
                    informations["Numéro"] = serie[0].strip()
                    informations["Album"] = serie[1].strip()
                else:
                    informations["Album"] = serie[0].strip()

    def _extract_additional_info(self, soup: BeautifulSoup, informations: dict) -> None:
        """ Extraire les informations supplémentaires """
        keys = ['Scénario', 'Dessin', 'Couleurs', 'Éditeur', 'Date de publication', 'Édition', 'Format']
        current_key = ""
        for tag in soup.find_all(['dt', 'dd']):
            if tag.name == 'dt':
                current_key = tag.get_text(strip=True)
                if current_key in informations:
                    current_key = None
            elif tag.name == 'dd' and current_key in keys:
                dd_text = " ".join(tag.stripped_strings)
                informations[current_key] = informations.get(current_key, "") + (
                    "," if current_key in informations else "") + dd_text

    def _extract_format_and_price(self, informations: dict, isbn: int) -> None:
        """ Extraire le format et le prix """
        if "Format" in informations:
            bd_info = informations.pop("Format")
            for value in bd_info.split("-"):
                if "pages" in value:
                    self._extract_pages(value, informations, isbn)
                elif "€" in value:
                    self._extract_price(value, informations, isbn)

    def _extract_pages(self, value: str, informations: dict, isbn: int) -> None:
        """ Extraire le nombre de planches """
        try:
            informations["Pages"] = int(value.replace("pages", "").strip())
        except ValueError:
            logger.warning(f"{value} est un nombre de planches incorrect", extra={"isbn": isbn})

    def _extract_price(self, value: str, informations: dict, isbn: int) -> None:
        """ Extraire le prix """
        try:
            informations["Prix"] = float(value.replace("€", "").strip())
        except ValueError:
            logger.warning(f"{value} est un prix incorrect", extra={"isbn": isbn})

    def _extract_image(self, soup: BeautifulSoup, informations: dict) -> None:
        """ Extraire l'image """
        meta_tag = soup.find('meta', attrs={'property': 'og:image'})
        if meta_tag:
            informations['Image'] = meta_tag['content']

    def _extract_synopsis(self, soup: BeautifulSoup, informations: dict) -> None:
        """ Extraire le synopsis """
        synopsis_tag = soup.find('p', class_='synopsis')
        if synopsis_tag:
            cleaned_synopsis = ''.join(str(tag) for tag in synopsis_tag.decode_contents()).strip().replace('\r',
                                                                                                           '').replace(
                '\n', '').replace('\t', '')
            informations["Synopsis"] = cleaned_synopsis

    def _parse_publication_date(self, informations: dict, isbn: int) -> None:
        """ Parse la date de publication """
        try:
            parsed_date = parse(self.translate(informations.get("Date de publication", "")),
                                dayfirst=True, fuzzy=True, default=datetime.datetime(1900, 1, 1))
            informations["Date de publication"] = parsed_date.date().isoformat()
        except ParserError:
            logger.warning("Problème de date de parution", extra={"isbn": isbn})

    def get_url(self, isbn: int) -> str:
        """Trouver lien BD bdphile.fr à partir de son ISBN"""

        search_link = "https://www.bdphile.fr/search/album/?q={}".format(isbn)
        html = self.get_html(search_link)
        soup = BeautifulSoup(html, 'html.parser')
        a_tag = soup.find('a', href=lambda href: href and href.startswith("https://www.bdphile.fr/album/view/"))
        if a_tag:
            return a_tag.get('href')
        else:
            raise AddAlbumError(f"ISBN {isbn} introuvable dans BD Phile")

    TRANSLATED_MONTHS = {
        "janvier": "January",
        "février": "February",
        "fevrier": "February",
        "mars": "March",
        "avril": "April",
        "mai": "May",
        "juin": "June",
        "juillet": "July",
        "août": "August",
        "aout": "August",
        "septembre": "September",
        "octobre": "October",
        "novembre": "November",
        "décembre": "December",
        "decembre": "December",
    }

    def translate(self, date: str) -> str:
        for mois, month in self.TRANSLATED_MONTHS.items():
            if mois in date.lower():
                date = date.lower().replace(mois, month)
        return date

    def get_html(self, url: str) -> str:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            logger.error(f"La requête a échoué. Statut de la réponse : {response.status_code}")
            raise AddAlbumError(f"Impossible d'affiche le code html de la page {url}")
