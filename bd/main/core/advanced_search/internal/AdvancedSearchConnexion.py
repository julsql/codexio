from django.db.models import QuerySet

from main.core.common.database.internal.bd_model import BD


class AdvancedSearchConnexion:

    def get_all(self) -> QuerySet[BD, BD]:
        return BD.objects.all()
