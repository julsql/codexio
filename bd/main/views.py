from django.http import JsonResponse
from django.shortcuts import render

from main.forms import RechercheForm
from main import recherche as recherche
from main import upload_photo
from django.views.decorators.csrf import csrf_exempt
from config.settings import POST_TOKEN
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
    banner, isbn_banner, random_type = recherche.banner()
    if request.method == 'POST':
        # créer une instance de notre formulaire et le remplir avec les données POST
        form = RechercheForm(request.POST)

        queryset = form_search(form)
        if queryset:
            infos = [{'ISBN': bd.isbn, 'Album': bd.Album, 'Numero': bd.Numéro, 'Serie': bd.Série} for bd in queryset]
            return render(request, 'main/bdrecherche.html', {'form': form, 'infos': infos})
        return render(request, 'main/home.html', {'form': form, 'infos': infos, 'banner': banner, 'isbn_banner': isbn_banner, "random_type": random_type})

    else:
        # ceci doit être une requête GET, donc créer un formulaire vide
        form = RechercheForm()

    return render(request, 'main/home.html', {'form': form, 'infos': infos, 'banner': banner, 'isbn_banner': isbn_banner, "random_type": random_type})


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


@csrf_exempt
def upload_dedicace(request, isbn):
    return upload_photo.upload_dedicace(request, isbn)


@csrf_exempt
def upload_exlibris(request, isbn):
    return upload_photo.upload_exlibris(request, isbn)


def delete_dedicace(request, isbn, photo_number):
    if request.method == 'GET':
        auth_header = request.headers.get('Authorization')
        if auth_header is None or auth_header != f"Bearer {POST_TOKEN}":
            return JsonResponse({'error': "Vous n'avez pas l'autorisation"})
        else:
            if upload_photo.delete_dedicace(isbn, photo_number) == 0:
                return JsonResponse({'message': "La photo n'a pas été trouvée"})
            else:
                return JsonResponse({'message': 'Dédicace supprimée correctement'})
    else:
        return JsonResponse({'message': 'Il faut une requête POST'})


def delete_exlibris(request, isbn, photo_number):
    if request.method == 'GET':
        auth_header = request.headers.get('Authorization')
        if auth_header is None or auth_header != f"Bearer {POST_TOKEN}":
            return JsonResponse({'error': "Vous n'avez pas l'autorisation"})
        else:
            if upload_photo.delete_exlibris(isbn, photo_number) == 0:
                return JsonResponse({'message': "La photo n'a pas été trouvée"})
            else:
                return JsonResponse({'message': 'Ex libris supprimé correctement'})
    else:
        return JsonResponse({'message': 'Il faut une requête POST'})
