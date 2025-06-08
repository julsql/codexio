from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

from main.core.application.usecases.advanced_search.advanced_search_service import AdvancedSearchService
from main.core.application.usecases.random_album.random_album_service import RandomAlbumService
from main.core.infrastructure.interface_adapters.views.formatters import convert_price
from main.core.infrastructure.persistence.database.advanced_search_adapter import AdvancedSearchAdapter
from main.core.infrastructure.persistence.database.random_album_adapter import RandomAlbumAdapter


@login_required
def home_view(request: HttpRequest) -> HttpResponse:
    if request.user.current_collection:
        collection = request.user.current_collection
    else:
        collection = request.user.collections.all().first()

    random_album_connexion = RandomAlbumAdapter()
    random_album_service = RandomAlbumService(random_album_connexion)
    random_album = random_album_service.main(collection)

    # Banner
    # random_attachment_repository = RandomAttachmentAdapter()
    # random_attachment_service = RandomAttachmentService(random_attachment_repository)
    # random_attachment = random_attachment_service.main()

    advanced_search_repository = AdvancedSearchAdapter()
    advanced_search_service = AdvancedSearchService(advanced_search_repository)
    advanced_search = advanced_search_service.main(request)

    if advanced_search.is_form_send:
        return render(request, 'bd_search/module.html')

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
                       'colorist': random_album.colorist,
                       'editor': random_album.publisher,
                       'publication_date': random_album.publication_date,
                       'edition': random_album.edition,
                       'number_of_pages': random_album.number_of_pages,
                       'purchase_price': convert_price(random_album.purchase_price),
                       'synopsis': random_album.synopsis,
                       'image': random_album.image}
                   })
