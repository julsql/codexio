from typing import Dict, Tuple, List

from main.core.advanced_search.internal.forms import RechercheForm
from main.core.common.database.internal.bd_model import BD


class AdvancedSearchService:
    def main(self, request) -> Tuple[RechercheForm, List[Dict[str, str]], bool]:
        if request.method == 'POST':
            form = RechercheForm(request.POST)
            infos = self.form_search(form)
            if infos:
                return form, infos, True
        else:
            form = RechercheForm()
            infos = self.form_search()
        return form, infos, False

    def form_search(self, form=None) -> List[Dict[str, str]]:
        queryset = BD.objects.all()

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

            for field_name, form_field_name in filters.items():
                value = data.get(form_field_name)
                if value:
                    queryset = queryset.filter(**{field_name: value})

            synopsis = data.get('synopsis')
            if synopsis:
                keywords = synopsis.split(" ")
                for keyword in keywords:
                    queryset = queryset.filter(synopsis__icontains=keyword)

            tri_par = data.get('tri_par')
            tri_croissant = data.get('tri_croissant')

            if tri_par:
                tri_par = tri_par if tri_croissant else f"-{tri_par}"
                queryset = queryset.order_by(tri_par)

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
