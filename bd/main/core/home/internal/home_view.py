from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

from main.application.usecases.advanced_search.advanced_search_service import AdvancedSearchService
from main.application.usecases.random_attachment.random_attachment_service import RandomAttachmentService
from main.infrastructure.persistence.database.random_album_adapter import RandomAlbumAdapter
from main.application.usecases.random_album.random_album_service import RandomAlbumService
from main.infrastructure.persistence.database.advanced_search_adapter import AdvancedSearchAdapter
from main.infrastructure.persistence.file.random_attachment_adapter import RandomAttachmentAdapter
from main.infrastructure.views.formatters import convert_price


def home(request: HttpRequest) -> HttpResponse:
    random_album_connexion = RandomAlbumAdapter()
    random_album_service = RandomAlbumService(random_album_connexion)
    random_album = random_album_service.main()

    random_attachment_repository = RandomAttachmentAdapter()
    random_attachment_service = RandomAttachmentService(random_attachment_repository)
    random_attachment = random_attachment_service.main()

    advanced_search_repository = AdvancedSearchAdapter()
    advanced_search_service = AdvancedSearchService(advanced_search_repository)
    advanced_search = advanced_search_service.main(request)

    if advanced_search.form_send:
        return render(request, 'bd_search/module.html',
                      {"banner_path": random_attachment.path, "banner_isbn": random_attachment.isbn,
                       "banner_type": random_attachment.type})

    if random_album.is_empty():
        return render(request, 'home/module.html',
                      {"banner_path": random_attachment.path,
                       "banner_isbn": random_attachment.isbn,
                       "banner_type": random_attachment.type,
                       "form": advanced_search.form})

    return render(request, 'home/module.html',
                  {"banner_path": random_attachment.path,
                   "banner_isbn": random_attachment.isbn,
                   "banner_type": random_attachment.type,
                   "form": advanced_search.form,
                   "random_album": {
                       'isbn': random_album.isbn,
                       'album': random_album.titre,
                       'number': random_album.numero,
                       'series': random_album.serie,
                       'writer': random_album.scenariste,
                       'illustrator': random_album.dessinateur,
                       'colorist': random_album.coloriste,
                       'editor': random_album.editeur,
                       'publication_date': random_album.date_publication,
                       'edition': random_album.edition,
                       'number_of_pages': random_album.nombre_pages,
                       'purchase_price': convert_price(random_album.prix),
                       'synopsis': random_album.synopsis,
                       'image': random_album.image_url}
                   })
