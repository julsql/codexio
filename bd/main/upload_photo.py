import os
import re

from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from bd.settings import POST_TOKEN

ALLOWED_EXTENSIONS = '.jpeg'
__FILEPATH__ = os.path.dirname(os.path.abspath(__file__))
DEDICACE_FOLDER = os.path.join(__FILEPATH__, 'static/main/images/dedicaces')
EXLIBRIS_FOLDER = os.path.join(__FILEPATH__, 'static/main/images/exlibris')

def allowed_file(filename):
    return '.' in filename and "." + filename.rsplit('.', 1)[1].lower() == ALLOWED_EXTENSIONS


def upload_dedicace(request, isbn):
    return upload(request, isbn, DEDICACE_FOLDER)


def upload_exlibris(request, isbn):
    return upload(request, isbn, EXLIBRIS_FOLDER)


def upload(request, isbn, origin_folder):
    if request.method == 'POST':
        auth_header = request.headers.get('Authorization')
        if auth_header is None or auth_header != f"Bearer {POST_TOKEN}":
            return JsonResponse({'error': f"Vous n'avez pas l'autorisation"})
        else:
            if 'file' in request.FILES:
                uploaded_file = request.FILES['file']
                if allowed_file(uploaded_file.name):
                    file_extension = os.path.splitext(uploaded_file.name)[1].lower()
                    path_folder = os.path.join(origin_folder, str(isbn))
                    number = get_next_number(path_folder)
                    fs = FileSystemStorage(location=path_folder)

                    fs.save(f"{number}{file_extension}", uploaded_file)
                    return JsonResponse({'message': f'Fichier {isbn} ajouté avec succès'})
                else:
                    return JsonResponse({'error': "Le type du fichier est incorrect"})
            else:
                return JsonResponse({'error': "Aucun fichier n'a été envoyé"})
    else:
        return JsonResponse({'message': 'Il faut une requête POST'})


def delete_photo(origin_folder, isbn, photo_number):
    album_path = os.path.join(origin_folder, str(isbn))
    image_path = os.path.join(album_path, f"{photo_number}{ALLOWED_EXTENSIONS}")
    if os.path.exists(image_path):
        os.remove(image_path)
        if not any(os.listdir(album_path)):
            os.rmdir(album_path)
        else:
            renommer_photos(album_path)
        return 1
    else:
        return 0


def renommer_photos(chemin_dossier):
    fichiers = os.listdir(chemin_dossier)

    fichiers_photos = [f for f in fichiers if f.endswith(ALLOWED_EXTENSIONS)]
    fichiers_photos.sort(key=lambda x: int(x.split('.')[0]))

    for i, fichier in enumerate(fichiers_photos, start=1):
        ancien_chemin = os.path.join(chemin_dossier, fichier)
        nouveau_nom = f"{i}{ALLOWED_EXTENSIONS}"
        nouveau_chemin = os.path.join(chemin_dossier, nouveau_nom)

        os.rename(ancien_chemin, nouveau_chemin)


def delete_dedicace(isbn, photo_number):
    return delete_photo(DEDICACE_FOLDER, isbn, photo_number)


def delete_exlibris(isbn, photo_number):
    return delete_photo(EXLIBRIS_FOLDER, isbn, photo_number)


def get_next_number(directory_path):
    if not os.path.isdir(directory_path):
        return 1

    image_paths = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_extension = os.path.splitext(file)[1].lower()
            if file_extension == ALLOWED_EXTENSIONS:
                image_paths.append(file)

    integers = [int(re.search(r'\d+', s).group()) for s in image_paths if re.search(r'\d+', s)]
    integers.sort()

    missing_integer = 1
    for num in integers:
        if num == missing_integer:
            missing_integer += 1
        elif num > missing_integer:
            break

    return missing_integer
