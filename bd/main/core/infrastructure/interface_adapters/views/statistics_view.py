from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from main.core.application.usecases.statistics.statistics_service import StatisticsService
from main.core.infrastructure.persistence.database.statistics_database_adapter import StatisticsDatabaseAdapter
from main.core.infrastructure.persistence.file.paths import SIGNED_COPY_FOLDER, EXLIBRIS_FOLDER
from main.core.infrastructure.persistence.file.statistics_attachment_adapter import StatisticsAttachmentAdapter


@login_required
def statistics_view(request: HttpRequest) -> HttpResponse:
    database_repository = StatisticsDatabaseAdapter()
    collection_id = request.user.collections.values('id').first()['id']

    attachment_repository = StatisticsAttachmentAdapter(SIGNED_COPY_FOLDER(collection_id),
                                                        EXLIBRIS_FOLDER(collection_id))

    service = StatisticsService(
        database_repository=database_repository,
        attachment_repository=attachment_repository
    )

    statistics = service.execute(request.user)

    return render(request, 'statistics/module.html', {
        'nombre': statistics.albums_count,
        'pages': statistics.pages_count,
        'prix': statistics.purchase_price_count,
        'tirage': statistics.deluxe_edition_count,
        'dedicaces': statistics.signed_copies_count,
        'exlibris': statistics.ex_libris_count,
        'title': "Lieu d'achat des albums",
        'places': statistics.place_of_purchase_pie,
    })
