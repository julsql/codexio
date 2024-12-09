from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from config.settings import DATABASES
from main.core.attachments.attachments_service import AttachmentsService
from main.core.common.database.internal.database_connexion import DatabaseConnexion


def attachments(request: HttpRequest) -> HttpResponse:
    database_file = DATABASES['default']['NAME']
    database = DatabaseConnexion(database_file)
    service = AttachmentsService(database)
    infos = service.main()
    return render(request, 'attachments/module.html', infos)
