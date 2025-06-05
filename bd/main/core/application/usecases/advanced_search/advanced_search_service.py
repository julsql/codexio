from main.core.application.forms.forms import RechercheForm
from main.core.domain.model.albums_from_form import AlbumsFromForm
from main.core.domain.model.reduce_album import ReduceAlbum
from main.core.domain.ports.repositories.advanced_search_repository import AdvancedSearchRepository


class AdvancedSearchService:
    def __init__(self, advanced_search_repository: AdvancedSearchRepository) -> None:
        self.repository = advanced_search_repository

    def main(self, request) -> AlbumsFromForm:
        if request.method == 'POST':
            form = RechercheForm(request.POST)
            infos = self.form_search(form)
            return AlbumsFromForm(form=form, albums=infos, is_form_send=True)
        else:
            form = RechercheForm()
            infos = self.form_search()
            return AlbumsFromForm(form=form, albums=infos, is_form_send=False)

    def form_search(self, form=None) -> list[ReduceAlbum]:
        queryset = self.repository.get_all()
        if form and form.is_valid():
            data = form.cleaned_data
            queryset = self.repository.get_by_form(data, queryset)

        return [
            ReduceAlbum(
                isbn=int(bd.isbn),
                title=bd.album,
                number=bd.number,
                series=bd.series,
                writer=bd.writer,
                illustrator=bd.illustrator,
            )
            for bd in queryset
        ]
