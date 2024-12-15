from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from main.core.attachments.attachments_service import AttachmentsService


def attachments(request: HttpRequest) -> HttpResponse:
    service = AttachmentsService()
    infos = service.main()
    return render(request, 'attachments/module.html', infos)
