from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from main.core.advanced_search.advanced_search_service import AdvancedSearchService
from main.core.advanced_search.internal.AdvancedSearchConnexion import AdvancedSearchConnexion


def bd_search(request: HttpRequest) -> HttpResponse:
    repository = AdvancedSearchConnexion()
    service = AdvancedSearchService(repository)
    form, infos, _ = service.main(request)
    return render(request, 'bd_search/module.html', {'form': form, 'infos': infos})
