from django.views.decorators.csrf import csrf_exempt

from main.core.advanced_search.advanced_search_service import AdvancedSearchService
from main.core.advanced_search.internal.advanced_search_connexion import AdvancedSearchConnexion
from main.core.advanced_search.internal.forms import RechercheForm


@csrf_exempt
def advanced_search(request) -> (RechercheForm, list[dict[str, str]], bool):
        repository = AdvancedSearchConnexion()
        service = AdvancedSearchService(repository)
        return service.main(request)
