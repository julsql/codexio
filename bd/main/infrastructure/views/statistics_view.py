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
        'nombre': statistics.albums_count,
        'pages': statistics.pages_count,
        'prix': statistics.purchase_price_count,
        'tirage': statistics.deluxe_edition_count,
        'dedicaces': statistics.signed_copies_count,
        'exlibris': statistics.ex_libris_count
    })
