from dataclasses import dataclass

from main.core.application.forms.bd_forms import RechercheBdForm
from main.core.application.forms.book_forms import RechercheBookForm
from main.core.domain.model.reduce_album import ReduceAlbum


@dataclass
class AlbumsFromForm:
    form: RechercheBdForm | RechercheBookForm
    albums: list[ReduceAlbum]
    is_form_send: bool

    def __str__(self) -> str:
        return f"RandomAlbumsFromForm(form={self.form}, albums={', '.join(str(album) for album in self.albums)}, is_form_send={self.is_form_send})"
