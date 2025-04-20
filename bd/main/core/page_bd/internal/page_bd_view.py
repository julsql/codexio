from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

from main.core.page_bd.page_bd_service import PageBdService


def page_bd(request: HttpRequest, isbn: int) -> HttpResponse:
    service = PageBdService()
    infos = service.main(isbn)
    if len(infos.keys()) == 1:
        return render(request, 'page_bd/not_found.html', infos)
    return render(request, 'page_bd/module.html', infos)
