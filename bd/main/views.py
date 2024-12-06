from django.shortcuts import render

from main.core.advanced_search.internal.advanced_search_view import advanced_search
from main.core.random_dedicace.internal.random_dedicace_view import random_dedicace
from main.forms import RechercheForm
from main import recherche as recherche
from main.models import BD


def form_search(form=None):
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

    return queryset


# Create your views here.
def home(request):
    infos = recherche.alea()
    banner = random_dedicace()
    form, form_send = advanced_search(request)
    value = banner.copy()
    if form_send:
        return render(request, 'main/bdrecherche.html', value)
    value.update({'form': form, 'infos': infos})
    return render(request, 'main/home.html', value)


def bdrecherche(request):
    if request.method == 'POST':
        # créer une instance de notre formulaire et le remplir avec les données POST
        form = RechercheForm(request.POST)
        queryset = form_search(form)
    else:
        # ceci doit être une requête GET, donc créer un formulaire vide
        form = RechercheForm()
        queryset = form_search()

    infos = [{'ISBN': bd.isbn, 'Album': bd.Album, 'Numero': bd.Numéro, 'Serie': bd.Série} for bd in queryset]
    return render(request, 'main/bdrecherche.html', {'form': form, 'infos': infos})


def dedicace(request):
    dedicaces, dedicaces_sum = recherche.dedicaces()
    exlibris, exlibris_sum = recherche.exlibris()
    return render(request, 'main/dedicace.html',
                  {'dedicaces': dedicaces, 'dedicaces_sum': dedicaces_sum,
                   'exlibris': exlibris, 'exlibris_sum': exlibris_sum})


def pagebd(request, isbn):
    try:
        infos = recherche.page(isbn)
    except:
        return render(request, 'main/bd_not_found.html', {"isbn": isbn})
    else:
        infos["dedicaces"] = recherche.dedicaces_album(isbn)
        infos["exlibris"] = recherche.exlibris_album(isbn)
        return render(request, 'main/pagebd.html', infos)


def statistiques(request):
    infos = recherche.stat()
    return render(request, 'main/statistiques.html', infos)
