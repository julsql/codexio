from django.http import HttpRequest

from main.core.application.forms.book_forms import RechercheBookForm
from main.core.domain.model.albums_from_form import AlbumsFromForm
from main.core.domain.model.reduce_album import ReduceAlbum
from main.core.domain.ports.repositories.advanced_search_repository import AdvancedSearchRepository


class AdvancedSearchBookService:
    def __init__(self, advanced_search_repository: AdvancedSearchRepository) -> None:
        self.repository = advanced_search_repository

    def main(self, request: HttpRequest, collection_id: int) -> AlbumsFromForm:
        if request.method == 'POST':
            form = RechercheBookForm(request.POST)
            infos = self.form_search(collection_id, form)
            return AlbumsFromForm(form=form, albums=infos, is_form_send=True)
        else:
            form = RechercheBookForm()
            infos = self.form_search(collection_id)
            return AlbumsFromForm(form=form, albums=infos, is_form_send=False)

    def form_search(self, collection_id: int, form=None) -> list[ReduceAlbum]:
        queryset = self.repository.get_all(collection_id)
        if form and form.is_valid():
            data = form.cleaned_data
            queryset = self.repository.get_by_form(data, queryset)

        return [
            ReduceAlbum(
                isbn=int(book.isbn),
                title=book.title,
                writer=book.writer,
            )
            for book in queryset
        ]
