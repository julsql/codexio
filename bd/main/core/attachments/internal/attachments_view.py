from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from config.settings import DATABASES
from main.core.attachments.attachments_service import AttachmentsService
from main.core.common.database.internal.database_connexion import DatabaseConnexion


def attachments(request: HttpRequest) -> HttpResponse:
    service = AttachmentsService()
    infos = service.main()
    return render(request, 'attachments/module.html', infos)
