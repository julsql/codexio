import re

import requests
from bs4 import BeautifulSoup

from main.core.add_album.add_album_error import AddAlbumError
from main.core.add_album.bd_repository import BdRepository
from main.core.common.logger.logger import logger


class BdGestRepository(BdRepository):
    SEARCH_URL = "https://www.bedetheque.com/search/albums"
    BANDEAU_CLASS = "bandeau-info album panier"
    IMAGE_CLASS = "bandeau-image album"
    BS_FEATURE = 'html.parser'

    def __str__(self) -> str:
        return "BdGestRepository"

    def get_infos(self, isbn: int) -> dict[str, str | float | int]:
        informations = {}
        url = self.get_url(isbn)

        html = self.get_html(url)
        soup = BeautifulSoup(html, self.BS_FEATURE)

        # Extraction du titre
        self._extract_title(soup, informations, isbn)

        # Extraction des informations sur les auteurs
        self._extract_authors(soup, informations, isbn)

        # Extraction des informations supplémentaires
        self._extract_additional_info(soup, informations, isbn)

        # Extraction le prix
        self._extract_price(soup, informations, isbn)

        # Image
        self._extract_image(soup, informations, isbn)

        # Synopsis
        self._extract_synopsis(soup, informations, isbn)

        # Date de publication
        self._parse_publication_date(informations, isbn)

        logger.info(informations, extra={"isbn": isbn})
        return informations

    def _extract_title(self, soup: BeautifulSoup, informations: dict, isbn: int) -> None:
        """ Extraire les informations du titre """
        full_title = self._get_input(soup, "AltTitle")
        if full_title:
            pattern = r'-([^-\s]+)-'
            match = re.search(pattern, full_title)

            if not match:
                raise ValueError("Format de titre invalide : le numéro de tome est introuvable")

            # Découpe aux positions trouvées
            tome = match.group(1)
            serie = full_title[:match.start()].strip()
            album = full_title[match.end():].strip()
            if tome:
                informations["Numéro"] = tome
            if serie:
                informations["Série"] = serie
            if album:
                informations["Album"] = album
        else:
            logger.warning("Impossible d'extraire le titre", extra={"isbn": isbn})
        return None

    def _extract_authors(self, soup: BeautifulSoup, informations: dict, isbn: int) -> None:
        """ Extraire les informations supplémentaires """
        keys = ['Scénario', 'Dessin', 'Couleurs']
        album_tag = soup.find("div", class_=self.BANDEAU_CLASS)
        if not album_tag:
            logger.warning("Informations supplémentaires non trouvées", extra={"isbn": isbn})
            return

        sub_title = album_tag.find("h3")
        if not sub_title:
            logger.warning("Éditeur non trouvé", extra={"isbn": isbn})
            return
        editor_tag = sub_title.find('span', {"itemprop": "publisher"})
        if not editor_tag:
            logger.warning("Éditeur non trouvé", extra={"isbn": isbn})
            return
        informations["Éditeur"] = editor_tag.get_text()

        auteur_tag = album_tag.find("div", class_="liste-auteurs")
        if not editor_tag:
            logger.warning("Créateurs non trouvés", extra={"isbn": isbn})
            return

        auteurs = auteur_tag.select("a")
        metiers = auteur_tag.select(".metier")

        # Remplir le dictionnaire avec les auteurs et leurs métiers
        for auteur, metier in zip(auteurs, metiers):
            nom = auteur.text.strip()
            if ", " in nom:
                name, surname = nom.split(", ")
                nom = f"{surname} {name}"

            categorie = metier.text.strip("()")  # Enlever les parenthèses
            if categorie in keys:
                informations[categorie] = nom

    def _extract_additional_info(self, soup: BeautifulSoup, informations: dict, isbn: int) -> None:
        """ Extraire les informations supplémentaires """

        album_tag = soup.find("div", class_=self.BANDEAU_CLASS)

        info_tag = album_tag.find("h4")
        date_tag = info_tag.find('span', {"title": "Dépot légal"}).get_text()

        # Vérifier s'il y a une date entre parenthèses (ex: 08 février 2023)
        match_precise = re.search(r"\((\d{2}) (\w+) (\d{4})\)", date_tag)

        if match_precise:
            # Si une date précise est trouvée, on la récupère
            jour, mois_fr, annee = match_precise.groups()
        else:
            # Sinon, on récupère la date générique au début (MM/YYYY)
            match_generale = re.search(r"(\d{2})/(\d{4})", date_tag)
            mois_fr, annee = match_generale.groups()
            jour = "01"  # On met par défaut le premier jour du mois

        informations['Date de publication'] = f"{annee}-{mois_fr}-{jour}"

        page_tag = info_tag.find('span', {"itemprop": "numberOfPages"}).get_text()

        try:
            informations["Pages"] = int(page_tag)
        except ValueError:
            logger.warning(f"{page_tag} est un nombre de planches incorrect", extra={"isbn": isbn})

    def _get_input(self, soup: BeautifulSoup, id: str):
        tag = soup.find("input", {"id": id})
        if tag:
            return tag.get("value")
        else:
            return None

    def _extract_price(self, soup: BeautifulSoup, informations: dict, isbn: int) -> None:
        """ Extraire le prix """
        album_id = self._get_input(soup, "IdAlbum")
        eans = self._get_input(soup, "EANs")
        ean = self._get_input(soup, "EAN")

        if album_id and eans and ean:
            url = f"https://www.bedetheque.com/ajax/album_bdfugue/idalbum/{album_id}/idbdfugue/{ean}/id/{eans}"
            response = requests.get(url)

            if response.status_code == 200:
                result = response.json()
                if 'price' in result:
                    informations["Prix"] = float(result['price'])
        else:
            logger.warning("Impossible d'extraire le prix", extra={"isbn": isbn})
        return None

    def _extract_image(self, soup: BeautifulSoup, informations: dict, isbn: int) -> None:
        """ Extraire l'image """
        body = soup.find("div", class_=self.IMAGE_CLASS)
        if not body:
            logger.warning("Image non trouvée", extra={"isbn": isbn})
            return
        a_tag = body.find("a") if body else None
        if not a_tag:
            logger.warning("Image non trouvée", extra={"isbn": isbn})
            return
        informations['Image'] = a_tag.get('href')

    def _extract_synopsis(self, soup: BeautifulSoup, informations: dict, isbn: int) -> None:
        """ Extraire le synopsis """

        synopsis_tag = soup.find('span', {"itemprop": "description"})
        if not synopsis_tag:
            logger.warning("Synopsis non trouvé", extra={"isbn": isbn})
            return
        informations["Synopsis"] = synopsis_tag.get_text()

    def get_url(self, isbn: int) -> str:
        """Trouver lien BD bdgest.fr à partir de son ISBN"""

        with requests.Session() as session:
            csrf_token = self.get_csrf_token(session)
            params = {
                "csrf_token_bel": csrf_token,
                "RechISBN": isbn
            }
            headers = {
                "User-Agent": "Mozilla/5.0",
                "Referer": self.SEARCH_URL
            }
            response = session.get(self.SEARCH_URL, params=params, headers=headers)

            if response.status_code != 200:
                logger.error(f"La requête a échoué. Statut de la réponse : {response.status_code}",
                             extra={"isbn": isbn})
                raise AddAlbumError(f"Impossible d'affiche le code html de la page {self.SEARCH_URL}")

            html = response.text

            soup = BeautifulSoup(html, self.BS_FEATURE)
            search_list = soup.find("ul", class_="search-list")

            # Trouver le premier <li> dans cette liste
            first_li = search_list.find("li") if search_list else None

            # Trouver la première balise <a> avec la classe "image-tooltip"
            a_tag = first_li.find("a", class_="image-tooltip") if first_li else None
            if a_tag:
                return a_tag.get('href')
            else:
                raise AddAlbumError(f"ISBN {isbn} introuvable dans BD Gest")

    def get_html(self, url: str) -> str:
        response = requests.get(url)
        # Vérifiez si la requête a réussi
        if response.status_code == 200:
            return response.text
        else:
            logger.error(f"La requête a échoué. Statut de la réponse : {response.status_code}")
            raise AddAlbumError(f"Impossible d'affiche le code html de la page {url}")

    def get_csrf_token(self, session):
        """Récupère dynamiquement le token CSRF depuis la page de recherche."""
        response = session.get(self.SEARCH_URL)

        if response.status_code != 200:
            raise AddAlbumError(f"Erreur {response.status_code} lors de l'accès au site.")

        soup = BeautifulSoup(response.text, self.BS_FEATURE)

        # Trouver le champ input contenant le token CSRF
        csrf_input = soup.find("input", {"name": "csrf_token_bel"})

        if csrf_input:
            return csrf_input["value"]
        else:
            raise AddAlbumError("Impossible de récupérer le token CSRF.")
