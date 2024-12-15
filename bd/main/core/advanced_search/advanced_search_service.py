from main.core.advanced_search.internal import AdvancedSearchConnexion
from main.core.advanced_search.internal.forms import RechercheForm


class AdvancedSearchService:
    def __init__(self, advanced_search_repository: AdvancedSearchConnexion) -> None:
        self.connexion = advanced_search_repository

    def main(self, request) -> (RechercheForm, list[dict[str, str]], bool):
        if request.method == 'POST':
            form = RechercheForm(request.POST)
            infos = self.form_search(form)
            if infos:
                return form, infos, True
        else:
            form = RechercheForm()
            infos = self.form_search()
            return form, infos, False

    def form_search(self, form=None) -> list[dict[str, str]]:
        queryset = self.connexion.get_all()

        if form and form.is_valid():
            data = form.cleaned_data

            filters = {
                'isbn__icontains': 'isbn',
                'album__icontains': 'album',
                'number__icontains': 'number',
                'series__icontains': 'series',
                'writer__icontains': 'writer',
                'illustrator__icontains': 'illustrator',
                'publisher__icontains': 'publisher',
                'edition__icontains': 'edition',
                'year_of_purchase': 'year_of_purchase',
                'signed_copy': 'signed_copy',
                'ex_libris': 'ex_libris',
            }

            # Appliquer les filtres à la requête
            for field_name, form_field_name in filters.items():
                value = data.get(form_field_name)
                if value:
                    queryset = queryset.filter(**{field_name: value})

            # Filtrer par synopsis si nécessaire
            synopsis = data.get('synopsis')
            if synopsis:
                keywords = synopsis.split()
                queryset = queryset.filter(synopsis__icontains=" ".join(keywords))

            # Appliquer le tri si nécessaire
            tri_par = data.get('tri_par')
            if tri_par:
                queryset = queryset.order_by(f"-{tri_par}" if not data.get('tri_croissant') else tri_par)

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
