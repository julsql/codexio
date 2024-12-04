from abc import ABC, abstractmethod
from typing import List
import requests

from main.core.add_album.add_album_error import AddAlbumError
from main.core.common.logger.logger import logger


class BdRepository(ABC):
    @abstractmethod
    def get_images(self, isbn: int) -> List:
        pass

    @abstractmethod
    def get_url(self, isbn: int) -> str:
        pass

    def get_html(self, url: str) -> str:
        response = requests.get(url)
        # Vérifiez si la requête a réussi
        if response.status_code == 200:
            return response.text
        else:
            logger.error(f"La requête a échoué. Statut de la réponse : {response.status_code}")
            raise AddAlbumError(f"Impossible d'affiche le code html de la page {url}")
