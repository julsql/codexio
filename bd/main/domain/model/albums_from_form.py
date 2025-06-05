from dataclasses import dataclass

from main.domain.forms.forms import RechercheForm
from main.domain.model.reduce_album import ReduceAlbum


@dataclass
class AlbumsFromForm:
    form: RechercheForm
    albums: list[ReduceAlbum]
    is_form_send: bool

    def __str__(self) -> str:
        return f"RandomAlbumsFromForm(form={self.form}, albums={', '.join(str(album) for album in self.albums)}, is_form_send={self.is_form_send})"
