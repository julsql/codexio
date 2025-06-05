import re
from decimal import Decimal

import requests
from bs4 import BeautifulSoup

from main.core.domain.exceptions.api_exceptions import ApiConnexionException, ApiConnexionRefused, \
    ApiConnexionDataNotFound
from main.core.domain.model.album import Album
from main.core.domain.ports.repositories.logger_repository import LoggerRepository
from main.core.infrastructure.api.base_album_adapter import BaseAlbumAdapter


class BdGestAdapter(BaseAlbumAdapter):
    SEARCH_URL = "https://www.bedetheque.com/search/albums"
    BANDEAU_CLASS = "bandeau-info album panier"
    IMAGE_CLASS = "bandeau-image album"
    BS_FEATURE = 'html.parser'

    def __init__(self, logger_repository: LoggerRepository) -> None:
        super().__init__(logger_repository)
        self.isbn = 0

    def __str__(self) -> str:
        return "BdGestRepository"

    def get_infos(self, isbn: int) -> Album:
        self.isbn = isbn
        album = Album(isbn=self.isbn)
        url = self.get_url()

        html = self.get_html(url)
        soup = BeautifulSoup(html, self.BS_FEATURE)

        # Extraction du titre
        self._extract_title(soup, album)

        # Extraction des informations sur les auteurs
        self._extract_authors(soup, album)

        # Extraction des informations supplémentaires
        self._extract_additional_info(soup, album)

        # Extraction le prix
        self._extract_price(soup, album)

        # Image
        self._extract_image(soup, album)

        # Synopsis
        self._extract_synopsis(soup, album)

        self.logging_repository.info(str(album), extra={"isbn": self.isbn})
        return album

    def _extract_title(self, soup: BeautifulSoup, album: Album) -> None:
        """ Extraire les informations du titre """
        full_title = self._get_input(soup, "AltTitle")
        if full_title:
            pattern = r'-([^-\s]+)-'
            match = re.search(pattern, full_title)

            if not match:
                raise ValueError("Format de titre invalide : le numéro de tome est introuvable")

            # Découpe aux positions trouvées
            tome = match.group(1)
            series = full_title[:match.start()].strip()
            titre = full_title[match.end():].strip()
            if tome:
                album.number = tome
            if series:
                album.series = series
            if album:
                album.title = titre
        else:
            self.logging_repository.warning("Impossible d'extraire le titre", extra={"isbn": self.isbn})
        return None

    def _extract_authors(self, soup: BeautifulSoup, album: Album) -> None:
        """ Extraire les informations supplémentaires """
        album_tag = soup.find("div", class_=self.BANDEAU_CLASS)
        if not album_tag:
            self.logging_repository.warning("Informations supplémentaires non trouvées", extra={"isbn": self.isbn})
            return

        sub_title = album_tag.find("h3")
        if not sub_title:
            self.logging_repository.warning("Éditeur non trouvé", extra={"isbn": self.isbn})
            return
        editor_tag = sub_title.find('span', {"itemprop": "publisher"})
        if not editor_tag:
            self.logging_repository.warning("Éditeur non trouvé", extra={"isbn": self.isbn})
            return
        album.publisher = editor_tag.get_text()

        auteur_tag = album_tag.find("div", class_="liste-auteurs")
        if not editor_tag:
            self.logging_repository.warning("Créateurs non trouvés", extra={"isbn": self.isbn})
            return

        auteurs = auteur_tag.select("a")
        metiers = auteur_tag.select(".metier")

        # Remplir le dictionnaire avec les auteurs et leurs métiers
        for auteur, metier in zip(auteurs, metiers):
            nom = auteur.text.strip()
            if ", " in nom:
                name, surname = nom.split(", ")
                nom = f"{surname} {name}"

            categories = metier.text.strip("()")
            match categories:
                case "Scénario":
                    album.writer = album.writer + ("," if album.writer != "" else "") + nom
                case "Dessin":
                    album.illustrator = album.illustrator + ("," if album.illustrator != "" else "") + nom
                case "Couleurs":
                    album.colorist = album.colorist + ("," if album.colorist != "" else "") + nom

    def _extract_additional_info(self, soup: BeautifulSoup, album: Album) -> None:
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

        date = f"{annee}-{mois_fr}-{jour}"
        album.publication_date = self._parse_publication_date(date, self.isbn)

        page = info_tag.find('span', {"itemprop": "numberOfPages"})
        if page:
            page_tag = page.get_text()
            try:
                album.number_of_pages = int(page_tag)
            except ValueError:
                self.logging_repository.warning(f"{page_tag} est un nombre de planches incorrect",
                                                extra={"isbn": self.isbn})

    def _get_input(self, soup: BeautifulSoup, id: str):
        tag = soup.find("input", {"id": id})
        if tag:
            return tag.get("value")
        else:
            return None

    def _extract_price(self, soup: BeautifulSoup, album: Album) -> None:
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
                    album.purchase_price = Decimal(result['price'])
        else:
            self.logging_repository.warning("Impossible d'extraire le prix", extra={"isbn": self.isbn})
        return None

    def _extract_image(self, soup: BeautifulSoup, album: Album) -> None:
        """ Extraire l'image """
        body = soup.find("div", class_=self.IMAGE_CLASS)
        if not body:
            self.logging_repository.warning("Image non trouvée", extra={"isbn": self.isbn})
            return
        a_tag = body.find("a") if body else None
        if not a_tag:
            self.logging_repository.warning("Image non trouvée", extra={"isbn": self.isbn})
            return
        album.image = a_tag.get('href')

    def _extract_synopsis(self, soup: BeautifulSoup, album: Album) -> None:
        """ Extraire le synopsis """
        album_id = self._get_input(soup, "IdAlbum")

        if album_id:
            url = f"https://www.bedetheque.com/ajax/resume/album/{album_id}"
            response = requests.get(url)

            if response.status_code == 200:
                result = response.text
                album.synopsis = result
        else:
            self.logging_repository.warning("Impossible d'extraire le synppsis", extra={"isbn": self.isbn})
        return None

    def get_url(self) -> str:
        """Trouver lien BD bdgest.fr à partir de son ISBN"""

        with requests.Session() as session:
            csrf_token = self.get_csrf_token(session)
            params = {
                "csrf_token_bel": csrf_token,
                "RechISBN": self.isbn
            }
            headers = {
                "User-Agent": "Mozilla/5.0",
                "Referer": self.SEARCH_URL
            }
            response = session.get(self.SEARCH_URL, params=params, headers=headers)

            if response.status_code != 200:
                self.logging_repository.error(f"La requête a échoué. Statut de la réponse : {response.status_code}",
                                              extra={"isbn": self.isbn})
                raise ApiConnexionException(f"Impossible d'affiche le code html de la page {self.SEARCH_URL}",
                                            str(self))

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
                raise ApiConnexionDataNotFound(f"ISBN {self.isbn} introuvable", str(self), self.isbn)

    def get_html(self, url: str) -> str:
        response = requests.get(url)
        # Vérifiez si la requête a réussi
        if response.status_code == 200:
            return response.text
        else:
            self.logging_repository.error(f"La requête a échoué. Statut de la réponse : {response.status_code}")
            raise ApiConnexionException(f"Impossible d'affiche le code html de la page {url}", str(self))

    def get_csrf_token(self, session):
        """Récupère dynamiquement le token CSRF depuis la page de recherche."""
        response = session.get(self.SEARCH_URL)
        print(self.SEARCH_URL)

        if response.status_code != 200:
            raise ApiConnexionException(f"Erreur {response.status_code} lors de l'accès au site.", str(self))

        soup = BeautifulSoup(response.text, self.BS_FEATURE)

        # Trouver le champ input contenant le token CSRF
        csrf_input = soup.find("input", {"name": "csrf_token_bel"})

        if csrf_input:
            return csrf_input["value"]
        else:
            raise ApiConnexionRefused("Impossible de récupérer le token CSRF.", str(self))
