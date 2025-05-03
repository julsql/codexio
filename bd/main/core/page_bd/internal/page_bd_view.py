from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

from main.core.page_bd.internal.page_bd_attachments_connexion import PageBdAttachmentsConnexion
from main.core.page_bd.internal.page_bd_database_connexion import PageBdDatabaseConnexion
from main.core.page_bd.page_bd_service import PageBdService


def page_bd(request: HttpRequest, isbn: int) -> HttpResponse:
    attachments_repository = PageBdAttachmentsConnexion()
    database_repository = PageBdDatabaseConnexion()
    service = PageBdService(attachments_repository, database_repository)
    infos = service.main(isbn)
    if len(infos.keys()) == 1:
        return render(request, 'page_bd/not_found.html', infos)
    return render(request, 'page_bd/module.html', infos)
