import datetime
import requests
import re
from bs4 import BeautifulSoup

from main.core.add_album.add_album_error import AddAlbumError
from main.core.add_album.bd_repository import BdRepository
from main.core.common.logger.logger import logger
from dateutil.parser import parse, ParserError


class BdGestRepository(BdRepository):
    SEARCH_URL = "https://www.bedetheque.com/search/albums"
    BANDEAU_CLASS = "bandeau-info album panier"
    IMAGE_CLASS = "bandeau-image album"

    def __init__(self) -> None:
        self.header = {"Titre album": "Album", "Tome": "Numéro",
                   "Série": "Série", "Scénario": "Scénario",
                   "Dessin": "Dessin", "Couleurs": "Couleurs", "Éditeur": "Éditeur",
                   "date de parution": "Date de publication", "": "Édition",
                   "Nombre de planches": "Pages"}

    def __str__(self) -> str:
        return "BdGestRepository"

    def get_infos(self, isbn: int) -> dict[str, str | float | int]:
        informations = {}
        url = self.get_url(isbn)

        html = self.get_html(url)
        soup = BeautifulSoup(html, 'html.parser')
        body = soup.find("div", class_="bandeau-principal")

        # Extraction du titre
        self._extract_title(soup, informations)

        # Extraction des informations sur les auteurs
        self._extract_authors(soup, informations)

        # Extraction des informations supplémentaires
        self._extract_additional_info(soup, informations)

        # Image
        self._extract_image(body, informations)

        # Synopsis
        self._extract_synopsis(soup, informations)

        # Date de publication
        self._parse_publication_date(informations, isbn)

        logger.info(informations, extra={"isbn": isbn})
        return informations

    def _extract_title(self, soup: BeautifulSoup, informations: dict) -> None:
        """ Extraire les informations du titre """
        album_tag = soup.find("div", class_=self.BANDEAU_CLASS)

        title = album_tag.find("h1")
        a_tag = title.find("a") if title else None
        if a_tag:
            informations['Série'] = a_tag.get('title')

        sub_title = album_tag.find("h2")
        if sub_title and sub_title.find("span", class_="numa"):
            sub_title.find("span", class_="numa").extract()

        # Récupérer le texte nettoyé

        sub_title = sub_title.text.split()
        if sub_title[0] == ".":
            sub_title = sub_title[1:]
        sub_title = " ".join(sub_title)

        informations['Album'] = sub_title

    def _extract_authors(self, soup: BeautifulSoup, informations: dict) -> None:
        """ Extraire les informations supplémentaires """
        keys = ['Scénario', 'Dessin', 'Couleurs']
        album_tag = soup.find("div", class_=self.BANDEAU_CLASS)

        sub_title = album_tag.find("h3")
        editor_tag = sub_title.find('span',{"itemprop": "publisher"})
        informations["Éditeur"] = editor_tag.get_text()

        auteur_tag = album_tag.find("div", class_="liste-auteurs")

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


    def _extract_additional_info(self, soup: BeautifulSoup, informations: dict) -> None:
        """ Extraire les informations supplémentaires """

        album_tag = soup.find("div", class_=self.BANDEAU_CLASS)

        info_tag = album_tag.find("h4")
        date_tag = info_tag.find('span',{"title": "Dépot légal"}).get_text()

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

        page_tag = info_tag.find('span',{"itemprop": "numberOfPages"}).get_text()

        try:
            informations["Pages"] = int(page_tag)
        except ValueError:
            logger.warning(f"{page_tag} est un nombre de planches incorrect")

    def _extract_price(self, value: str, informations: dict, isbn: int) -> None:
        """ Extraire le prix """
        return None

    def _extract_image(self, soup: BeautifulSoup, informations: dict) -> None:
        """ Extraire l'image """

        body = soup.find("div", class_=self.IMAGE_CLASS)
        a_tag = body.find("a") if body else None
        if a_tag:
            informations['Image'] = a_tag.get('href')

    def _extract_synopsis(self, soup: BeautifulSoup, informations: dict) -> None:
        """ Extraire le synopsis """

        synopsis_tag = soup.find('span',{"itemprop": "description"})
        if synopsis_tag:
            informations["Synopsis"] = synopsis_tag.get_text()

    def _parse_publication_date(self, informations: dict, isbn: int) -> None:
        """ Parse la date de publication """
        try:
            parsed_date = parse(self.translate(informations.get("Date de publication", "")),
                                dayfirst=True, fuzzy=True, default=datetime.datetime(1900, 1, 1))
            informations["Date de publication"] = parsed_date.date().isoformat()
        except ParserError:
            logger.warning("Problème de date de parution", extra={"isbn": isbn})

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
                logger.error(f"La requête a échoué. Statut de la réponse : {response.status_code}")
                raise AddAlbumError(f"Impossible d'affiche le code html de la page {self.SEARCH_URL}")

            html = response.text

            soup = BeautifulSoup(html, 'html.parser')
            search_list = soup.find("ul", class_="search-list")

            # Trouver le premier <li> dans cette liste
            first_li = search_list.find("li") if search_list else None

            # Trouver la première balise <a> avec la classe "image-tooltip"
            a_tag = first_li.find("a", class_="image-tooltip") if first_li else None
            if a_tag:
                return a_tag.get('href')
            else:
                raise AddAlbumError(f"ISBN {isbn} introuvable dans BD Gest")

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
            raise Exception(f"Erreur {response.status_code} lors de l'accès au site.")

        soup = BeautifulSoup(response.text, 'html.parser')

        # Trouver le champ input contenant le token CSRF
        csrf_input = soup.find("input", {"name": "csrf_token_bel"})

        if csrf_input:
            return csrf_input["value"]
        else:
            raise Exception("Impossible de récupérer le token CSRF.")