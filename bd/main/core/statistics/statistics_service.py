from typing import Dict

from main.core.common.database.database_repository import DatabaseRepository

class StatisticsService:
    def __init__(self, database_repository: DatabaseRepository) -> None:
        self.database = database_repository

    def main(self) -> Dict[str, int]:
        self.database.open()
        infos = self.database.get_one("SELECT COUNT(*) AS nombre, "
                                  "CAST(SUM(\"Nombre de pages\") AS INTEGER) AS pages, "
                                  "CAST(SUM(Dédicace) AS INTEGER) AS dedicaces, "
                                  "CAST(SUM(\"Ex Libris\") AS INTEGER) AS exlibris, "
                                  "CAST(SUM(Cote) AS INTEGER) AS prix "
                                  "FROM BD;")
        infos.update(self.database.get_one("SELECT COUNT(*) AS tirage FROM BD WHERE LOWER(\"Tirage de tête\") = 'oui';"))
        self.database.close()
        return infos
