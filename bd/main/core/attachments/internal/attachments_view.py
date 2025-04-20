from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

from main.core.attachments.attachments_service import AttachmentsService


def signed_copies(request: HttpRequest) -> HttpResponse:
    service = AttachmentsService()
    infos = service.main_signed_copies()
    return render(request, 'attachments/signed_copies.html', infos)


def exlibris(request: HttpRequest) -> HttpResponse:
    service = AttachmentsService()
    infos = service.main_ex_libris()
    return render(request, 'attachments/exlibris.html', infos)
