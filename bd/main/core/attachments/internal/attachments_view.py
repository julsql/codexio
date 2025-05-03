from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

from main.core.attachments.attachments_service import AttachmentsService
from main.core.attachments.internal.attachments_connexion import AttachmentsConnexion


def signed_copies(request: HttpRequest) -> HttpResponse:
    repository = AttachmentsConnexion()
    service = AttachmentsService(repository)
    infos = service.main_signed_copies()
    return render(request, 'attachments/module.html', infos)


def exlibris(request: HttpRequest) -> HttpResponse:
    repository = AttachmentsConnexion()
    service = AttachmentsService(repository)
    infos = service.main_ex_libris()
    return render(request, 'attachments/module.html', infos)
