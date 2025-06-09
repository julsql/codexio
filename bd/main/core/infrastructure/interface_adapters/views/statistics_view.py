from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from main.core.application.usecases.statistics.statistics_service import StatisticsService
from main.core.domain.model.profile_type import ProfileType
from main.core.infrastructure.interface_adapters.profile_type.profile_type_adapter import ProfileTypeAdapter
from main.core.infrastructure.interface_adapters.responses.request_response_adapter import RequestResponseAdapter
from main.core.infrastructure.persistence.database.statistics_database_adapter import StatisticsDatabaseAdapter
from main.core.infrastructure.persistence.file.paths import SIGNED_COPY_FOLDER, EXLIBRIS_FOLDER
from main.core.infrastructure.persistence.file.statistics_attachment_adapter import StatisticsAttachmentAdapter


class StatisticsView:
    def __init__(self):
        self.response_adapter = RequestResponseAdapter()
        self.profile_type_adapter = ProfileTypeAdapter(self.response_adapter)

    def handle_request(self, request: HttpRequest) -> HttpResponse:
        database_repository = StatisticsDatabaseAdapter()
        if request.user.current_collection:
            collection = request.user.current_collection
        else:
            collection = request.user.collections.all().first()

        attachment_repository = StatisticsAttachmentAdapter(SIGNED_COPY_FOLDER(collection.id),
                                                            EXLIBRIS_FOLDER(collection.id))


        service = StatisticsService(
            database_repository=database_repository,
            attachment_repository=attachment_repository
        )

        statistics = service.execute(collection)

        signed_copies = statistics.signed_copies_count
        exlibris = statistics.ex_libris_count

        profile_type = self.profile_type_adapter.get_profile_type(collection)
        if not isinstance(profile_type, ProfileType):
            return profile_type

        if profile_type == ProfileType.BD:
            work_type = "bande dessinée"
            work_type_plur = "bandes dessinées"
        elif profile_type == ProfileType.BOOK:
            exlibris = None
            work_type = "livre"
            work_type_plur = "livres"
        else:
            return self.response_adapter.technical_error("Erreur dans la recherche de profils")

        return render(request, 'statistics/module.html', {
            'nombre': statistics.albums_count,
            'pages': statistics.pages_count,
            'prix': statistics.purchase_price_count,
            'tirage': statistics.deluxe_edition_count,
            'dedicaces': signed_copies,
            'exlibris': exlibris,
            'title': f"Lieu d'achat des {work_type_plur}",
            'places': statistics.place_of_purchase_pie,
            'work_type': work_type
        })


@login_required
def statistics_view(request: HttpRequest) -> HttpResponse:
    view = StatisticsView()
    return view.handle_request(request)
