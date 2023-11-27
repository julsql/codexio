from django.http import JsonResponse
from django.shortcuts import render
from main.forms import RechercheForm
from main import recherche as recherche
from main import upload
from django.views.decorators.csrf import csrf_exempt
from main.add_album import sheet_add_album
from main.add_album import sheet_connection
from bd.settings import POST_TOKEN
from main.update_database import update
import os


# Create your views here.
def home(request):
    infos = recherche.alea()
    banner, isbn_banner, random_type = recherche.banner()
    if request.method == 'POST':
        # créer une instance de notre formulaire et le remplir avec les données POST
        form = RechercheForm(request.POST)

        if form.is_valid():
            isbn = request.POST.get('isbn')
            titre = request.POST.get('titre')
            num = request.POST.get('id_numero')
            serie = request.POST.get('id_serie')
            scenariste = request.POST.get('id_scenariste')
            dessinateur = request.POST.get('id_dessinateur')
            editeur = request.POST.get('id_editeur')
            edition = request.POST.get('id_edition')
            annee = request.POST.get('id_annee')
            dedicace = request.POST.get('id_dedicace')
            exlibris = request.POST.get('id_exlibris')
            synopsis = request.POST.get('id_synopsis')

            infos = recherche.recherche_bd(isbn, titre, num, serie, scenariste, dessinateur, editeur, edition, annee,
                                           dedicace, exlibris, synopsis)
            return render(request, 'main/bdrecherche.html', {'form': form, 'infos': infos})
        return render(request, 'main/home.html', {'form': form, 'infos': infos, 'banner': banner, 'isbn_banner': isbn_banner, "random_type": random_type})
    # si le formulaire n'est pas valide, nous laissons l'exécution continuer jusqu'au return
    # ci-dessous et afficher à nouveau le formulaire (avec des erreurs).

    else:
        # ceci doit être une requête GET, donc créer un formulaire vide
        form = RechercheForm()

    return render(request, 'main/home.html', {'form': form, 'infos': infos, 'banner': banner, 'isbn_banner': isbn_banner, "random_type": random_type})


def bdrecherche(request):
    if request.method == 'POST':
        # créer une instance de notre formulaire et le remplir avec les données POST
        form = RechercheForm(request.POST)

        if form.is_valid():
            isbn = request.POST.get('isbn')
            titre = request.POST.get('titre')
            num = request.POST.get('numero')
            serie = request.POST.get('serie')
            scenariste = request.POST.get('scenariste')
            dessinateur = request.POST.get('dessinateur')
            editeur = request.POST.get('editeur')
            edition = request.POST.get('edition')
            annee = request.POST.get('annee')
            dedicace = request.POST.get('dedicace')
            exlibris = request.POST.get('exlibris')
            synopsis = request.POST.get('synopsis')

            infos = recherche.recherche_bd(isbn, titre, num, serie, scenariste, dessinateur, editeur, edition, annee,
                                           dedicace, exlibris, synopsis)
        else:
            infos = recherche.recherche_bd()
    else:
        # ceci doit être une requête GET, donc créer un formulaire vide
        form = RechercheForm()
        infos = recherche.recherche_bd()

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
        print(infos)
        return render(request, 'main/pagebd.html', infos)


def statistiques(request):
    infos = recherche.stat()
    return render(request, 'main/statistiques.html', infos)


@csrf_exempt
def upload_dedicace(request, isbn):
    return upload.upload_dedicace(request, isbn)


@csrf_exempt
def upload_exlibris(request, isbn):
    return upload.upload_exlibris(request, isbn)


def delete_dedicace(request, isbn, photo_number):
    if request.method == 'GET':
        auth_header = request.headers.get('Authorization')
        if auth_header is None or auth_header != f"Bearer {POST_TOKEN}":
            return JsonResponse({'error': f"Vous n'avez pas l'autorisation"})
        else:
            if upload.delete_dedicace(isbn, photo_number) == 0:
                return JsonResponse({'message': "La photo n'a pas été trouvée"})
            else:
                return JsonResponse({'message': 'Ex libris supprimé correctement'})
    else:
        return JsonResponse({'message': 'Il faut une requête POST'})


def delete_exlibris(request, isbn, photo_number):
    if request.method == 'GET':
        auth_header = request.headers.get('Authorization')
        if auth_header is None or auth_header != f"Bearer {POST_TOKEN}":
            return JsonResponse({'error': f"Vous n'avez pas l'autorisation"})
        else:
            if upload.delete_exlibris(isbn, photo_number) == 0:
                return JsonResponse({'message': "La photo n'a pas été trouvée"})
            else:
                return JsonResponse({'message': 'Ex libris supprimé correctement'})
    else:
        return JsonResponse({'message': 'Il faut une requête POST'})


def update_database(request):
    if request.method == 'GET':
        auth_header = request.headers.get('Authorization')
        if auth_header is None or auth_header != f"Bearer {POST_TOKEN}":
            return JsonResponse({'error': f"Vous n'avez pas l'autorisation"})
        else:
            update()
            return JsonResponse({'message': 'Site web mis à jour correctement'})
    else:
        return JsonResponse({'message': 'Il faut une requête POST'})


def add_album(request, isbn):
    if request.method == 'GET':
        auth_header = request.headers.get('Authorization')
        if auth_header is None or auth_header != f"Bearer {POST_TOKEN}":
            return JsonResponse({'error': f"Vous n'avez pas l'autorisation"})
        else:
            infos = sheet_add_album.add_album(isbn)
            if type(infos) is not type({}):
                return JsonResponse({'error': str(infos)})
            elif infos:
                return JsonResponse({'message': f'Album {isbn} ajouté avec succès'})
            else:
                return JsonResponse({'error': f"Erreur d'ajout de l'album {isbn}"})
    else:
        return JsonResponse({'message': 'Il faut une requête POST'})


def possede(request, isbn):
    if request.method == 'GET':
        doc_name = "bd"
        sheet_name = "BD"
        connection = sheet_connection.Conn("logs.txt")
        connection.open(doc_name, sheet_name)
        if connection.double(isbn):
            message = f"Album {isbn} déjà enregistré"
        else:
            message = f"Album {isbn} jamais enregistré"
        return JsonResponse({'message': message}, charset='utf-8')
