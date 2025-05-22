from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from main.application.usecases.statistics.statistics_service import StatisticsService
from main.infrastructure.persistence.database.statistics_database_adapter import StatisticsDatabaseAdapter
from main.infrastructure.persistence.file.statistics_attachment_adapter import StatisticsAttachmentAdapter


def statistics_view(request: HttpRequest) -> HttpResponse:
    database_repository = StatisticsDatabaseAdapter()
    attachment_repository = StatisticsAttachmentAdapter()

    service = StatisticsService(
        database_repository=database_repository,
        attachment_repository=attachment_repository
    )

    statistics = service.execute()

    return render(request, 'statistics/module.html', {
        'nombre': statistics.nombre_albums,
        'pages': statistics.nombre_pages,
        'prix': statistics.prix_total,
        'tirage': statistics.nombre_editions_speciales,
        'dedicaces': statistics.nombre_dedicaces,
        'exlibris': statistics.nombre_exlibris
    })
