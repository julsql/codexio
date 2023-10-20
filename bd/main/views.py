from django.http import JsonResponse
from django.shortcuts import render
from main.forms import RechercheForm
from main import recherche as recherche
from main import upload
from django.views.decorators.csrf import csrf_exempt
from main.add_album import sheet_add_album
from main.add_album.error import Error
from bd.settings import POST_TOKEN

# update_database.update()


# Create your views here.
def home(request):
    infos = recherche.alea()
    banner = recherche.banner()
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
        return render(request, 'main/home.html', {'form': form, 'infos': infos, 'banner': banner})
    # si le formulaire n'est pas valide, nous laissons l'exécution continuer jusqu'au return
    # ci-dessous et afficher à nouveau le formulaire (avec des erreurs).

    else:
        # ceci doit être une requête GET, donc créer un formulaire vide
        form = RechercheForm()

    return render(request, 'main/home.html', {'form': form, 'infos': infos, 'banner': banner})


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
    dedicaces = recherche.dedicaces()
    exlibris = recherche.exlibris()
    return render(request, 'main/dedicace.html', {'dedicaces': dedicaces, 'exlibris': exlibris})


def pagebd(request, isbn):
    try:
        infos = recherche.page(isbn)
        return render(request, 'main/pagebd.html', infos)
    except:
        # La bd n'existe pas
        return render(request, 'main/bd_not_found.html', {"isbn": isbn})


def statistiques(request):
    infos = recherche.stat()
    return render(request, 'main/statistiques.html', infos)


@csrf_exempt
def upload_dedicace(request, isbn):
    return upload.upload_dedicace(request, isbn)


@csrf_exempt
def upload_exlibris(request, isbn):
    return upload.upload_exlibris(request, isbn)


def add_album(request, isbn):
    print(request.META)
    Error(str(request.META))
    Error(request.META['HTTP_AUTHORIZATION'])
    if 'HTTP_AUTHORIZATION' in request.META and request.META['HTTP_AUTHORIZATION'] == f'Bearer {POST_TOKEN}':
        if request.method == 'GET':

            infos = sheet_add_album.add_album(isbn)
            if infos:
                return JsonResponse({'message': 'Album added successfully', "infos": infos})
            else:
                return JsonResponse({'message': 'Error in the adding of the album'})
        else:
            return JsonResponse({'message': 'Please make a GET request'})
    else:
        return JsonResponse({'error': "You don't have the authorization"})
