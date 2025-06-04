from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

from main.application.usecases.page_bd.page_bd_service import PageBdService
from main.infrastructure.logging.python_logger_adapter import PythonLoggerAdapter
from main.infrastructure.persistence.database.page_bd_database_adapter import PageBdDatabaseAdapter
from main.infrastructure.persistence.file.page_bd_attachments_adapter import PageBdAttachmentsAdapter
from main.infrastructure.persistence.file.paths import SIGNED_COPY_FOLDER, EXLIBRIS_FOLDER
from main.infrastructure.views.formatters import convert_price


class PageBdView:
    def __init__(self):
        self.logger_adapter = PythonLoggerAdapter()

    def handle_request(self, request: HttpRequest, isbn: int) -> HttpResponse:
        attachments_repository = PageBdAttachmentsAdapter(SIGNED_COPY_FOLDER, EXLIBRIS_FOLDER)
        database_repository = PageBdDatabaseAdapter()
        service = PageBdService(attachments_repository, database_repository, self.logger_adapter)
        infos = service.main(isbn)
        if not infos:
            return render(request, 'page_bd/not_found.html', {"isbn": isbn})
        return render(request, 'page_bd/module.html', {
            'isbn': infos.album.isbn,
            'album': infos.album.album,
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
            "dedicaces": infos.attachment.dedicaces,
            "nb_dedicace": len(infos.attachment.dedicaces),
            "ex_libris": infos.attachment.ex_libris,
            "nb_exlibris": len(infos.attachment.ex_libris),
        })


def page_bd_view(request: HttpRequest, isbn: int) -> HttpResponse:
    view = PageBdView()
    return view.handle_request(request, isbn)
