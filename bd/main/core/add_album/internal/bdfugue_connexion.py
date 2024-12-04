import re
from typing import Dict, Any

import requests
from bs4 import BeautifulSoup

from main.core.add_album.add_album_error import AddAlbumError
from main.core.add_album.bd_repository import BdRepository
from main.core.common.logger.logger import logger


class BdFugueRepository(BdRepository):

    def __init__(self):
        self.header = {"Titre album": "Album", "Tome": "Numéro",
                   "Série": "Série", "Scénario": "Scénario",
                   "Dessin": "Dessin", "Couleurs": "Couleurs", "Éditeur": "Éditeur",
                   "date de parution": "Date de publication", "": "Édition",
                   "Nombre de pages": "Pages"}

    def __str__(self) -> str:
        return "BdFugueRepository"

    def get_infos(self, isbn: int) -> Dict[str, Any]:
        url = self.get_url(isbn)
        logger.info(url, extra={"isbn": isbn})
        html = self.get_html(url)
        soup = BeautifulSoup(html, 'html.parser')

        error_div = soup.find('title', text=re.compile(r'^Résultats de recherche pour :'))
        if error_div:
            raise AddAlbumError(f"{isbn} n'est pas dans BD Fugue ou il y a ambiguïté", isbn)

        infos = {}

        divs = soup.find_all("div", {"class": ["col label w-1/3 product-attribute-label truncate",
                                               "col data w-2/3 product-attribute-value font-semibold"]})
        for i in range(0, len(divs), 2):
            label = divs[i].text.strip().split(":")[0].strip()
            value = divs[i + 1].text.strip()
            if label == "Auteur(s)":
                personnes = value.split(" , ")
                for personne in personnes:
                    match = re.search(r'^([\w\s-]+)\s+\(([^)]+)\)', personne.strip())
                    if match:
                        nom = match.group(1)
                        attributs = [attr.strip() for attr in match.group(2).split(',')]
                        for fonction in attributs:
                            if fonction in self.header.keys():
                                if fonction in infos:
                                    infos[fonction] += "," + nom
                                else:
                                    infos[fonction] = nom
            elif label == "Format narratif":
                if value == "Intégrale" or value == "Histoire complète":
                    infos["Numéro"] = 1

            elif label in self.header.keys():
                if self.header[label] == "Pages":
                    try:
                        infos[self.header[label]] = int(value)
                    except ValueError:
                        logger.warning("Pas de nombre de page correct trouvé", extra={"isbn": isbn})
                else:
                    infos[self.header[label]] = value

        if "Album" not in infos and "Série" in infos:
            infos["Album"] = infos["Série"]

        meta_tag = soup.find("meta", {"property": "product:price:amount"})
        no_price_error_message = "Pas de prix correct trouvé"
        if meta_tag:
            try:
                infos["Prix"] = float(meta_tag.get("content"))
            except ValueError:
                meta_tag = soup.find("meta", {"itemprop": "price"})
                if meta_tag:
                    try:
                        infos["Prix"] = float(meta_tag.get("content"))
                    except ValueError:
                        logger.warning(no_price_error_message, extra={"isbn": isbn})
                else:
                    logger.warning(no_price_error_message, extra={"isbn": isbn})
        else:
            meta_tag = soup.find("meta", {"itemprop": "price"})
            if meta_tag:
                try:
                    infos["Prix"] = float(meta_tag.get("content"))
                except ValueError:
                    logger.warning(no_price_error_message, extra={"isbn": isbn})
            else:
                logger.warning(no_price_error_message, extra={"isbn": isbn})

        pattern = re.compile(r'https://www\.bdfugue\.com/media/catalog/product/cache/.*')
        image_element = soup.find('img', {'src': pattern})

        if image_element:
            infos["Image"] = image_element.get('src')
        else:
            logger.warning("Pas d'image trouvée", extra={"isbn": isbn})

        div_tag = soup.find("div", {"itemprop": "description"})

        if div_tag:
            infos["Synopsis"] = div_tag.get_text(strip=True)
        else:
            logger.warning("Pas de synopsis trouv", extra={"isbn": isbn})

        return infos

    def get_url(self, isbn: int) -> str:
        return f"https://www.bdfugue.com/catalogsearch/result/?q={isbn}"

    def get_html(self, url: str) -> str:
        response = requests.get(url)
        # Vérifiez si la requête a réussi
        if response.status_code == 200:
            return response.text
        else:
            logger.error(f"La requête a échoué. Statut de la réponse : {response.status_code}")
            raise AddAlbumError(f"Impossible d'affiche le code html de la page {url}")
