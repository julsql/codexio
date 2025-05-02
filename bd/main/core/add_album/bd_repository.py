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
        date_string = informations.get("Date de publication", "")

        if not date_string:
            return

        # Vérifier d'abord si la date est déjà au format ISO
        try:
            datetime.strptime(date_string, "%Y-%m-%d")
            return
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
                    informations["Date de publication"] = f"{annee}-{mois}-{int(jour):02d}"
                    return None

            # Utiliser dateutil.parser comme fallback
            parsed_date = parse(date_string, dayfirst=True, fuzzy=True)
            informations["Date de publication"] = parsed_date.strftime("%Y-%m-%d")
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
