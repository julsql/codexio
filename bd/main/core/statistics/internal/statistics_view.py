from django.shortcuts import render

from config.settings import DATABASES
from main.core.common.database.internal.database_connexion import DatabaseConnexion
from main.core.statistics.statistics_service import StatisticsService


def statistiques(request):
    database_file = DATABASES['default']['NAME']
    database = DatabaseConnexion(database_file)
    service = StatisticsService(database)
    infos = service.main()
    return render(request, 'statistics/module.html', infos)
