from typing import Dict, Tuple

from main.core.advanced_search.advanced_search_service import AdvancedSearchService
from main.forms import RechercheForm


def advanced_search(request) -> Tuple[Dict[str, str] | RechercheForm, bool]:
    if request.method == 'POST':
        form = RechercheForm(request.POST)
        service = AdvancedSearchService()
        infos = service.main(form)
        if infos:
            return infos, True
    else:
        form = RechercheForm()
    return form, False
