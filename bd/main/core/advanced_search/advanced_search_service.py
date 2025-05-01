from main.core.advanced_search.advanced_search_repository import AdvancedSearchRepository
from main.core.advanced_search.internal.forms import RechercheForm


class AdvancedSearchService:
    def __init__(self, advanced_search_repository: AdvancedSearchRepository) -> None:
        self.repository = advanced_search_repository

    def main(self, request) -> (RechercheForm, list[dict[str, str]], bool):
        if request.method == 'POST':
            form = RechercheForm(request.POST)
            infos = self.form_search(form)
            return form, infos, len(infos), True
        else:
            form = RechercheForm()
            infos = self.form_search()
            return form, infos, len(infos), False

    def form_search(self, form=None) -> list[dict[str, str]]:
        queryset = self.repository.get_all()
        if form and form.is_valid():
            data = form.cleaned_data
            queryset = self.repository.get_by_form(data, queryset)

        return [
            {
                'ISBN': bd.isbn,
                'Album': bd.album,
                'Numero': bd.number,
                'Serie': bd.series,
                'Scenariste': bd.writer,
                'Dessinateur': bd.illustrator,
            }
            for bd in queryset
        ]
