from typing import Dict, Tuple, List

from main.core.advanced_search.internal.forms import RechercheForm
from main.core.advanced_search.internal.models import BD


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
                'Album__icontains': 'titre',
                'Numéro__icontains': 'numero',
                'Série__icontains': 'serie',
                'Scénariste__icontains': 'scenariste',
                'Dessinateur__icontains': 'dessinateur',
                'Éditeur__icontains': 'editeur',
                'Édition__icontains': 'edition',
                'Année_d_achat': 'annee',
                'Dédicace': 'dedicace',
                'Ex_Libris': 'exlibris',
            }

            for field_name, form_field_name in filters.items():
                value = data.get(form_field_name)
                if value:
                    queryset = queryset.filter(**{field_name: value})

            synopsis = data.get('synopsis').split(" ")
            for mot in synopsis:
                queryset = queryset.filter(Synopsis__icontains=mot)

            tri_par = data.get('tri_par')
            tri_croissant = data.get('tri_croissant')

            if tri_par:
                tri_par = tri_par if tri_croissant else f"-{tri_par}"
                queryset = queryset.order_by(tri_par)

        return [{'ISBN': bd.isbn, 'Album': bd.Album, 'Numero': bd.Numéro, 'Serie': bd.Série} for bd in queryset]
