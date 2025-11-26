from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

from main.core.application.usecases.advanced_search.advanced_search_bd_service import AdvancedSearchBdService
from main.core.application.usecases.advanced_search.advanced_search_book_service import AdvancedSearchBookService
from main.core.application.usecases.random_album.random_album_service import RandomAlbumService
from main.core.domain.model.profile_type import ProfileType
from main.core.infrastructure.interface_adapters.profile_type.profile_type_adapter import ProfileTypeAdapter
from main.core.infrastructure.interface_adapters.responses.request_response_adapter import RequestResponseAdapter
from main.core.infrastructure.interface_adapters.views.formatters import convert_price
from main.core.infrastructure.persistence.database.advanced_search_bd_adapter import AdvancedSearchBdAdapter
from main.core.infrastructure.persistence.database.advanced_search_book_adapter import AdvancedSearchBookAdapter
from main.core.infrastructure.persistence.database.random_bd_adapter import RandomBdAdapter
from main.core.infrastructure.persistence.database.random_book_adapter import RandomBookAdapter


class HomeView:
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
            advanced_search_repository = AdvancedSearchBdAdapter()
            advanced_search_service = AdvancedSearchBdService(advanced_search_repository)
            advanced_search = advanced_search_service.main(request, collection.id)

            random_album_connexion = RandomBdAdapter()

        elif profile_type == ProfileType.BOOK:
            advanced_search_repository = AdvancedSearchBookAdapter()
            advanced_search_service = AdvancedSearchBookService(advanced_search_repository)
            advanced_search = advanced_search_service.main(request, collection.id)

            random_album_connexion = RandomBookAdapter()
        else:
            return self.response_adapter.technical_error("Erreur dans la recherche de profils")

        if advanced_search.is_form_send:
            return render(request, 'album_search/module.html')

        random_album_service = RandomAlbumService(random_album_connexion)
        random_album = random_album_service.main(collection.id)

        if random_album.is_empty():
            return render(request, 'home/module.html',
                          {"form": advanced_search.form})

        return render(request, 'home/module.html',
                      {"form": advanced_search.form,
                       "random_album": {
                           'isbn': random_album.isbn,
                           'album': random_album.title,
                           'number': random_album.number,
                           'series': random_album.series,
                           'writer': random_album.writer,
                           'illustrator': random_album.illustrator,
                           'publication_date': random_album.publication_date,
                           'number_of_pages': random_album.number_of_pages,
                           'purchase_price': convert_price(random_album.purchase_price),
                           'synopsis': random_album.synopsis,
                           'image': random_album.image}
                       })

@login_required
def home_view(request: HttpRequest) -> HttpResponse:
    view = HomeView()
    return view.handle_request(request)
