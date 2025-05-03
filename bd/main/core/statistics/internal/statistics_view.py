from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from main.core.statistics.internal.statistics_attachments_connexion import StatisticsAttachmentsConnexion
from main.core.statistics.internal.statistics_database_connexion import StatisticsDatabaseConnexion
from main.core.statistics.statistics_service import StatisticsService


def statistiques(request: HttpRequest) -> HttpResponse:
    attachments_repository = StatisticsAttachmentsConnexion()
    database_repository = StatisticsDatabaseConnexion()

    service = StatisticsService(attachments_repository, database_repository)
    infos = service.main()
    return render(request, 'statistics/module.html', infos)
