from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from main.core.application.usecases.advanced_search.advanced_search_service import AdvancedSearchService
from main.core.domain.model.profile_type import ProfileType
from main.core.infrastructure.interface_adapters.profile_type.profile_type_adapter import ProfileTypeAdapter
from main.core.infrastructure.interface_adapters.responses.request_response_adapter import RequestResponseAdapter
from main.core.infrastructure.persistence.database.advanced_search_adapter import AdvancedSearchAdapter


class SearchView:
    def __init__(self):
        self.response_adapter = RequestResponseAdapter()
        self.profile_type_adapter = ProfileTypeAdapter(self.response_adapter)

    def handle_request(self, request: HttpRequest) -> HttpResponse:
        if request.user.current_collection:
            collection = request.user.current_collection
        else:
            collection = request.user.collections.all().first()

        profile_type = self.profile_type_adapter.get_profile_type(collection)
        if not isinstance(profile_type, ProfileType):
            return profile_type

        if profile_type == ProfileType.BD:
            repository = AdvancedSearchAdapter()
            service = AdvancedSearchService(repository)
            advanced_search = service.main(request, collection.id)
            return render(request, 'bd_search/module.html',
                          {'form': advanced_search.form,
                           'infos': [{'ISBN': search_result.isbn,
                                      'Album': search_result.title,
                                      'Numero': search_result.number,
                                      'Serie': search_result.series
                                      } for search_result in advanced_search.albums],
                           'total': len(advanced_search.albums)})
        elif profile_type == ProfileType.BOOK:
            return self.response_adapter.technical_error("Impossible de rechercher des livres pour le moment")
        else:
            return self.response_adapter.technical_error("Erreur dans la recherche de profils")


@login_required
def search_view(request: HttpRequest) -> HttpResponse:
    view = SearchView()
    return view.handle_request(request)
