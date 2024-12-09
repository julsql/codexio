from django.shortcuts import render

from main.core.advanced_search.advanced_search_service import AdvancedSearchService

def bd_search(request):
    service = AdvancedSearchService()
    form, infos, _ = service.main(request)
    return render(request, 'bd_search/module.html', {'form': form, 'infos': infos})
