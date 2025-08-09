from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

from main.core.application.usecases.page_bd.page_bd_service import BdService
from main.core.application.usecases.page_book.page_book_service import BookService
from main.core.domain.model.profile_type import ProfileType
from main.core.infrastructure.interface_adapters.profile_type.profile_type_adapter import ProfileTypeAdapter
from main.core.infrastructure.interface_adapters.responses.request_response_adapter import RequestResponseAdapter
from main.core.infrastructure.interface_adapters.views.formatters import convert_price
from main.core.infrastructure.logging.python_logger_adapter import PythonLoggerAdapter
from main.core.infrastructure.persistence.database.page_bd_database_adapter import WorkDatabaseBdAdapter
from main.core.infrastructure.persistence.database.page_book_database_adapteur import WorkDatabaseBookAdapter
from main.core.infrastructure.persistence.file.page_bd_attachments_adapter import WorkAttachmentsAdapter
from main.core.infrastructure.persistence.file.paths import SIGNED_COPY_FOLDER, EXLIBRIS_FOLDER


class WorkView:
    def __init__(self):
        self.logger_adapter = PythonLoggerAdapter()
        self.response_adapter = RequestResponseAdapter()
        self.profile_type_adapter = ProfileTypeAdapter(self.response_adapter)

    def handle_request(self, request: HttpRequest, isbn: int) -> HttpResponse:
        if request.user.current_collection:
            collection = request.user.current_collection
        else:
            collection = request.user.collections.all().first()

        profile_type = self.profile_type_adapter.get_profile_type(collection)
        if not isinstance(profile_type, ProfileType):
            return profile_type

        if profile_type == ProfileType.BD:
            attachments_repository = WorkAttachmentsAdapter(SIGNED_COPY_FOLDER(collection.id),
                                                            EXLIBRIS_FOLDER(collection.id))
            database_repository = WorkDatabaseBdAdapter()
            service = BdService(attachments_repository, database_repository, self.logger_adapter)
            infos = service.main(isbn, collection.id)
            if not infos:
                return render(request, 'page_bd/not_found.html', {"isbn": isbn})
            return render(request, 'page_bd/module.html', {
                'isbn': infos.album.isbn,
                'album': infos.album.title,
                'number': infos.album.number,
                'series': infos.album.series,
                'writer': infos.album.writer,
                'illustrator': infos.album.illustrator,
                'colorist': infos.album.colorist,
                'publisher': infos.album.publisher,
                'publication_date': infos.album.publication_date,
                'edition': infos.album.edition,
                'number_of_pages': infos.album.number_of_pages,
                'rating': convert_price(infos.album.rating),
                'purchase_price': convert_price(infos.album.purchase_price),
                'year_of_purchase': infos.album.year_of_purchase,
                'place_of_purchase': infos.album.place_of_purchase,
                'deluxe_edition': infos.album.deluxe_edition,
                'localisation': infos.album.localisation,
                'synopsis': infos.album.synopsis,
                'image': infos.album.image,
                "dedicaces": infos.attachments.signed_copies,
                "nb_dedicace": len(infos.attachments.signed_copies),
                "ex_libris": infos.attachments.ex_libris,
                "nb_exlibris": len(infos.attachments.ex_libris),
                "collection_id": collection.id,
            })
        elif profile_type == ProfileType.BOOK:
            attachments_repository = WorkAttachmentsAdapter(SIGNED_COPY_FOLDER(collection.id),
                                                            EXLIBRIS_FOLDER(collection.id))
            database_repository = WorkDatabaseBookAdapter()
            service = BookService(attachments_repository, database_repository, self.logger_adapter)
            infos = service.main(isbn, collection.id)
            if not infos:
                return render(request, 'page_book/not_found.html', {"isbn": isbn})
            return render(request, 'page_book/module.html', {
                'isbn': infos.album.isbn,
                'title': infos.album.title,
                'writer': infos.album.writer,
                'translator': infos.album.translator,
                'publisher': infos.album.publisher,
                'collection_book': infos.album.collection_book,
                'publication_date': infos.album.publication_date,
                'edition': infos.album.edition,
                'number_of_pages': infos.album.number_of_pages,
                'literary_genre': infos.album.literary_genre,
                'style': infos.album.style,
                'origin_language': infos.album.origin_language,
                'purchase_price': convert_price(infos.album.purchase_price),
                'year_of_purchase': infos.album.year_of_purchase,
                'place_of_purchase': infos.album.place_of_purchase,
                'localisation': infos.album.localisation,
                'synopsis': infos.album.synopsis,
                'image': infos.album.image,
                "dedicaces": infos.attachments.signed_copies,
                "nb_dedicace": len(infos.attachments.signed_copies),
                "collection_id": collection.id,
            })
        else:
            return self.response_adapter.technical_error("Erreur dans la recherche de profils")


@login_required
def work_view(request: HttpRequest, isbn: int) -> HttpResponse:
    view = WorkView()
    return view.handle_request(request, isbn)
