from main.core.advanced_search.advanced_search_service import AdvancedSearchService
from main.core.advanced_search.internal.AdvancedSearchConnexion import AdvancedSearchConnexion
from main.core.advanced_search.internal.forms import RechercheForm


def advanced_search(request) -> (RechercheForm, list[dict[str, str]], bool):
        repository = AdvancedSearchConnexion()
        service = AdvancedSearchService(repository)
        return service.main(request)
