from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from main.core.statistics.statistics_service import StatisticsService


def statistiques(request: HttpRequest) -> HttpResponse:
    service = StatisticsService()
    infos = service.main()
    return render(request, 'statistics/module.html', infos)
