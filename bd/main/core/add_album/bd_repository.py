import re
from abc import ABC, abstractmethod
from datetime import datetime

from dateutil.parser import parse

from main.core.common.logger.logger import logger


class BdRepository(ABC):
    @abstractmethod
    def get_infos(self, isbn: int) -> dict[str, str | float | int]:
        pass

    @abstractmethod
    def get_url(self, isbn: int) -> str:
        pass

    @abstractmethod
    def get_html(self, url: str) -> str:
        pass

    def _parse_publication_date(self, informations: dict, isbn: int) -> None:
        """ Parse la date de publication """
        publication_date_key = "Date de publication"

        date_string = informations.get(publication_date_key, "")

        if not date_string:
            return None

        # Essaie d'abord le format complet YYYY-MM-DD
        try:
            informations[publication_date_key] = datetime.strptime(date_string, "%Y-%m-%d").strftime("%Y-%m-%d")
            return None
        except ValueError:
            pass

        # Essaie le format YYYY-MM
        try:
            informations[publication_date_key] = datetime.strptime(date_string, "%Y-%m").strftime("%Y-%m-01")
            return None
        except ValueError:
            pass

        # Essaie le format YYYY
        try:
            if re.match(r'^\d{4}$', date_string):
                informations[publication_date_key] = f"{date_string}-01-01"
                return None
        except ValueError:
            pass

        date_string = self.translate(date_string)

        # Dictionnaire des mois en français
        mois_fr = {
            "janv": "01", "janvier": "01",
            "févr": "02", "fev": "02", "février": "02",
            "mars": "03",
            "avr": "04", "avril": "04",
            "mai": "05",
            "juin": "06",
            "juil": "07", "juillet": "07",
            "août": "08", "aout": "08",
            "sept": "09", "septembre": "09",
            "oct": "10", "octobre": "10",
            "nov": "11", "novembre": "11",
            "déc": "12", "décembre": "12"
        }

        try:
            # Format "8 févr. 2023"
            if '.' in date_string:
                jour, mois, annee = date_string.replace('.', '').split()
                if mois.lower() in mois_fr:
                    mois = mois_fr[mois.lower()]
                    informations[publication_date_key] = f"{annee}-{mois}-{int(jour):02d}"
                    return None

            parsed_date = parse(date_string, dayfirst=True, fuzzy=True)

            # Vérifie le niveau de précision de la date originale
            if re.match(r'^\d{4}$', date_string):
                # Seulement l'année
                informations[publication_date_key] = f"{parsed_date.year}-01-01"
            elif re.match(r'^\d{4}-\d{1,2}$', date_string) or len(date_string.split()) == 2:
                # Année et mois seulement
                informations[publication_date_key] = f"{parsed_date.year}-{parsed_date.month:02d}-01"
            else:
                # Date complète
                informations[publication_date_key] = parsed_date.strftime("%Y-%m-%d")
            return None

        except ValueError:
            logger.warning(f"Problème de parsing de la date: {date_string}", extra={"isbn": isbn})
            return None

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
