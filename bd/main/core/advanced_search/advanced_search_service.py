from typing import Dict

from main.models import BD


class AdvancedSearchService:
    def main(self, form) -> Dict[str, str]:
        return self.form_search(form)

    def form_search(self, form=None) -> Dict[str, str]:
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

        infos = [{'ISBN': bd.isbn, 'Album': bd.Album, 'Numero': bd.Numéro, 'Serie': bd.Série} for bd in queryset]

        return infos
