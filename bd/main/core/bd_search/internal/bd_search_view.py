from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from main.core.advanced_search.advanced_search_service import AdvancedSearchService
from main.core.advanced_search.internal.advanced_search_connexion import AdvancedSearchConnexion


@csrf_exempt
def bd_search(request: HttpRequest) -> HttpResponse:
    repository = AdvancedSearchConnexion()
    service = AdvancedSearchService(repository)
    form, infos, _ = service.main(request)
    return render(request, 'bd_search/module.html', {'form': form, 'infos': infos})
