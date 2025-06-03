from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from main.application.usecases.advanced_search.advanced_search_service import AdvancedSearchService
from main.infrastructure.persistence.database.advanced_search_adapter import AdvancedSearchAdapter


@csrf_exempt
def bd_search(request: HttpRequest) -> HttpResponse:
    repository = AdvancedSearchAdapter()
    service = AdvancedSearchService(repository)
    advanced_search = service.main(request)
    return render(request, 'bd_search/module.html',
                  {'form': advanced_search.form,
                   'infos': [{'ISBN': search_result.isbn,
                              'Album': search_result.titre,
                              'Numero': search_result.numero,
                              'Serie': search_result.serie,
                              'Scenariste': search_result.scenariste,
                              'Dessinateur': search_result.dessinateur
                              } for search_result in advanced_search.albums],
                   'total': len(advanced_search.albums)})
