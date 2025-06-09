from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from main.core.application.usecases.advanced_search.advanced_search_service import AdvancedSearchService
from main.core.infrastructure.persistence.database.advanced_search_adapter import AdvancedSearchAdapter


@login_required
def bd_search_view(request: HttpRequest) -> HttpResponse:
    repository = AdvancedSearchAdapter()
    service = AdvancedSearchService(repository)
    advanced_search = service.main(request)
    return render(request, 'bd_search/module.html',
                  {'form': advanced_search.form,
                   'infos': [{'ISBN': search_result.isbn,
                              'Album': search_result.title,
                              'Numero': search_result.number,
                              'Serie': search_result.series
                              } for search_result in advanced_search.albums],
                   'total': len(advanced_search.albums)})
