from typing import Dict, Tuple, List

from main.core.advanced_search.advanced_search_service import AdvancedSearchService
from main.forms import RechercheForm


def advanced_search(request) -> Tuple[RechercheForm, List[Dict[str, str]], bool]:
        service = AdvancedSearchService()
        return service.main(request)
