from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render
from main.forms import RechercheForm
from main import recherche as recherche
import os
import re


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
    infos = recherche.page(isbn)
    return render(request, 'main/pagebd.html', infos)


def statistiques(request):
    infos = recherche.stat()
    return render(request, 'main/statistiques.html', infos)


ALLOWED_EXTENSIONS = 'jpeg'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == ALLOWED_EXTENSIONS


def upload_dedicace(request, isbn):
    __FILEPATH__ = os.path.dirname((os.path.dirname(os.path.abspath(__file__))))
    DEDICACE_FOLDER = os.path.join(__FILEPATH__, 'static/main/images/dedicaces')
    return upload(request, isbn, DEDICACE_FOLDER)


def upload_exlibris(request, isbn):
    __FILEPATH__ = os.path.dirname((os.path.dirname(os.path.abspath(__file__))))
    EXLIBRIS_FOLDER = os.path.join(__FILEPATH__, 'static/main/images/exlibris')
    return upload(request, isbn, EXLIBRIS_FOLDER)


def upload(request, isbn, origin_folder):
    if request.method == 'POST' and 'file' in request.FILES:
        uploaded_file = request.FILES['file']
        if allowed_file(uploaded_file.name):
            fs = FileSystemStorage(location=origin_folder)
            fs.save(f"{isbn}/{uploaded_file.name}", uploaded_file)
            return JsonResponse({'message': 'File uploaded successfully'})
        else:
            return JsonResponse({'error': 'File type not allowed'})
    else:
        return JsonResponse({'error': 'No file part or no selected file'})


def get_next_number(directory_path):
    if not os.path.isdir(directory_path):
        return []

    image_paths = []
    allowed_image_extensions = ".jpeg"

    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_extension = os.path.splitext(file)[1].lower()
            if file_extension == allowed_image_extensions:
                image_path = os.path.join(root, file)
                image_paths.append(image_path)

    integers = [int(re.search(r'\d+', s).group()) for s in image_paths if re.search(r'\d+', s)]
    integers.sort()

    missing_integer = 1
    for num in integers:
        if num == missing_integer:
            missing_integer += 1
        elif num > missing_integer:
            break

    return missing_integer
