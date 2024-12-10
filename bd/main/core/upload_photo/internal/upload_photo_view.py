import os
from config.settings import STATIC_ROOT

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from config.settings import POST_TOKEN
from main.core.upload_photo.internal.photo_connexion import PhotoConnexion
from main.core.upload_photo.upload_photo_service import UploadPhotoService


@csrf_exempt
def upload_dedicace(request, isbn: int):
    return upload_photo(request, isbn, "dedicaces")

@csrf_exempt
def upload_exlibris(request, isbn: int):
    return upload_photo(request, isbn, "exlibris")

def upload_photo(request, isbn: int, photo_type: str):
    if request.method == 'POST':
        auth_header = request.headers.get('Authorization')
        if auth_header is None or auth_header != f"Bearer {POST_TOKEN}":
            return JsonResponse({'error': "Vous n'avez pas l'autorisation"})
        else:
            if 'file' in request.FILES:
                uploaded_file = request.FILES['file']
                dedicace_folder = os.path.join(STATIC_ROOT, 'main/images/dedicaces')
                exlibris_folder = os.path.join(STATIC_ROOT, 'main/images/exlibris')
                photo_repository = PhotoConnexion(dedicace_folder, exlibris_folder)
                service = UploadPhotoService(photo_repository)
                if service.main(isbn, uploaded_file, photo_type):
                    return JsonResponse({'message': f'Photo {isbn} ajoutée avec succès'})
                else:
                    return JsonResponse({'error': "Le type du fichier est incorrect"})
            else:
                return JsonResponse({'error': "Aucun fichier n'a été envoyé"})
    else:
        return JsonResponse({'message': 'Il faut une requête POST'})
