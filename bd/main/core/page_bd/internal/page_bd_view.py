from django.http import HttpResponse
from django.shortcuts import render
from config.settings import DATABASES
from main.core.common.database.internal.database_connexion import DatabaseConnexion
from main.core.page_bd.page_bd_service import PageBdService


def page_bd(request, isbn) -> HttpResponse:
    service = PageBdService()
    infos = service.main(isbn)
    if len(infos.keys()) == 1:
        return render(request, 'page_bd/not_found.html', infos)
    return render(request, 'page_bd/module.html', infos)
