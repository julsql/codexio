from typing import Any

from django.db.models import QuerySet

from main.domain.ports.repositories.advanced_search_repository import AdvancedSearchRepository
from main.infrastructure.persistence.database.models import BD


class InMemoryAdvancedSearchRepository(AdvancedSearchRepository):
    def __init__(self):
        self.bds = []
        self._mock_queryset = None

    def add_bd(self, isbn: str, album: str, number: str, series: str,
               writer: str, illustrator: str) -> None:
        """Méthode utilitaire pour ajouter des BDs pour les tests"""
        bd = BD()
        bd.isbn = isbn
        bd.album = album
        bd.number = number
        bd.series = series
        bd.writer = writer
        bd.illustrator = illustrator
        self.bds.append(bd)

    def get_all(self) -> QuerySet[BD, BD]:
        """Simule QuerySet.all()"""
        # Convertit la liste en un mock de QuerySet
        self._mock_queryset = MockQuerySet(self.bds)
        return self._mock_queryset

    def get_by_form(self, data: dict[str, Any], queryset: QuerySet[BD, BD]) -> QuerySet[BD, BD]:
        """Simule le filtrage par formulaire"""
        filtered_bds = []

        for bd in self.bds:
            matches = True

            if 'isbn' in data and data['isbn']:
                matches = matches and data['isbn'].lower() in bd.isbn.lower()
            if 'album' in data and data['album']:
                matches = matches and data['album'].lower() in bd.title.lower()
            if 'number' in data and data['number']:
                matches = matches and data['number'].lower() in bd.number.lower()
            if 'series' in data and data['series']:
                matches = matches and data['series'].lower() in bd.series.lower()
            if 'writer' in data and data['writer']:
                matches = matches and data['writer'].lower() in bd.writer.lower()
            if 'illustrator' in data and data['illustrator']:
                matches = matches and data['illustrator'].lower() in bd.illustrator.lower()

            if matches:
                filtered_bds.append(bd)

        return MockQuerySet(filtered_bds)

    def order_by(self, queryset: QuerySet[BD], criteria: bool, croissant: bool) -> QuerySet[BD]:
        """Simule l'ordonnancement"""
        if not criteria:
            return queryset

        bds = list(queryset)
        reverse = not croissant

        # Tri par série puis par numéro
        bds.sort(key=lambda x: (x.series, x.number), reverse=reverse)
        return MockQuerySet(bds)


class MockQuerySet:
    """Classe utilitaire pour simuler un QuerySet Django"""

    def __init__(self, data):
        self.data = data

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, item):
        return self.data[item]

    def filter(self, **_kwargs):
        # Implémentation simple du filtre si nécessaire
        return self
