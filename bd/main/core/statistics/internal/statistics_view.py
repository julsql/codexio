from django.shortcuts import render

from config.settings import DATABASES
from main.core.common.database.internal.database_connexion import DatabaseConnexion
from main.core.statistics.statistics_service import StatisticsService


def statistiques(request):
    service = StatisticsService()
    infos = service.main()
    return render(request, 'statistics/module.html', infos)
