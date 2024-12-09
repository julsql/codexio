from typing import Dict

from config.settings import DATABASES
from main.core.common.database.internal.database_connexion import DatabaseConnexion
from main.core.random_album.random_album_service import RandomAlbumService


def random_album() -> Dict[str, str]:
    database_file = DATABASES['default']['NAME']
    database = DatabaseConnexion(database_file)
    service = RandomAlbumService(database)
    return service.main()
