from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from main.core.application.usecases.advanced_search.advanced_search_service import AdvancedSearchService
from main.core.infrastructure.persistence.database.advanced_search_adapter import AdvancedSearchAdapter


@csrf_exempt
def bd_search_view(request: HttpRequest) -> HttpResponse:
    repository = AdvancedSearchAdapter()
    service = AdvancedSearchService(repository)
    advanced_search = service.main(request)
    return render(request, 'bd_search/module.html',
                  {'form': advanced_search.form,
                   'infos': [{'ISBN': search_result.isbn,
                              'Album': search_result.title,
                              'Numero': search_result.number,
                              'Serie': search_result.series,
                              'Scenariste': search_result.writer,
                              'Dessinateur': search_result.illustrator
                              } for search_result in advanced_search.albums],
                   'total': len(advanced_search.albums)})
