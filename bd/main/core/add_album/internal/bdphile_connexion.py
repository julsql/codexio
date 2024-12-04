from typing import Dict

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

    def get_infos(self, isbn: int) -> Dict:
        informations = {}
        url = self.get_url(isbn)
        html = self.get_html(url)
        soup = BeautifulSoup(html, 'html.parser')

        title_tag = soup.find('title')

        if title_tag:
            title_text = title_tag.get_text()
            elements = title_text.split("|")[0].strip()

            elements = elements.split(" - ")
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

        keys = ['Scénario', 'Dessin', 'Couleurs', 'Éditeur', 'Date de publication', 'Édition', 'Format']
        current_key = ""
        for tag in soup.find_all(['dt', 'dd']):
            if tag.name == 'dt':
                current_key = tag.get_text(strip=True)
                if current_key in informations.keys():
                    current_key = None
            elif tag.name == 'dd' and current_key in keys:
                    dd_text = " ".join(tag.stripped_strings)
                    if current_key in informations.keys():
                        informations[current_key] += "," + dd_text
                    else:
                        informations[current_key] = dd_text

        try:
            parsed_date = parse(self.translate(informations["Date de publication"]),
                                       dayfirst=True, fuzzy=True, default=datetime.datetime(1900, 1, 1))
            informations["Date de publication"] = parsed_date.date().isoformat()
        except ParserError:
            logger.warning("Problème de date de parution", extra={"isbn": isbn})

        if "Format" in informations:
            bd_info = informations["Format"]
            informations.pop("Format")
            format_list = bd_info.split("-")
            for value in format_list:
                if "pages" in value:
                    try:
                        informations["Pages"] = int(value.replace("pages", "").strip())
                    except ValueError:
                        logger.warning(f"{value} est un nombre de pages incorrect", extra={"isbn": isbn})

                if "€" in value:
                    try:
                        informations["Prix"] = float(value.replace("€", "").strip())
                    except ValueError:
                        logger.warning(f"{value} est un prix incorrect", extra={"isbn": isbn})

        meta_tag = soup.find('meta', attrs={'property': 'og:image'})
        if meta_tag:
            informations['Image'] = meta_tag['content']

        synopsis_tag = soup.find('p', class_='synopsis')
        if synopsis_tag:
            cleaned_synopsis = ''.join(str(tag) for tag in synopsis_tag.decode_contents()).strip().replace('\r',
                                                                                                           '').replace(
                '\n', '').replace('\t', '')
            informations["Synopsis"] = cleaned_synopsis

        logger.info(informations, extra={"isbn": isbn})
        return informations

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
