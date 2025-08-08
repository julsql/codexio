from abc import ABC, abstractmethod

from django.db.models import QuerySet

from main.core.domain.model.statistics import Statistics


class StatisticsDatabaseRepository(ABC):
    @abstractmethod
    def get_database_statistics(self, collection_id: int) -> Statistics:
        pass

    def map_place_of_purchase(self, place_of_purchase_query: QuerySet) -> list[tuple[str, int]]:
        all_results = list(place_of_purchase_query)
        first_to_show = 4

        top_4 = all_results[:first_to_show]
        others = all_results[first_to_show:]

        place_of_purchase_stats = [(item['place_of_purchase'], item['count']) for item in top_4]
        other_total = sum(item['count'] for item in others)
        if other_total > 0:
            place_of_purchase_stats.append(("AUTRE", other_total))
        return place_of_purchase_stats