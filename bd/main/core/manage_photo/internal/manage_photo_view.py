from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from config.settings import POST_TOKEN
from main.core.manage_photo.delete_photo_service import DeletePhotoService
from main.core.manage_photo.upload_photo_service import UploadPhotoService


@csrf_exempt
def upload_dedicace(request, isbn: int):
    return upload_photo(request, isbn, "dedicaces")

@csrf_exempt
def upload_exlibris(request, isbn: int):
    return upload_photo(request, isbn, "exlibris")

def delete_dedicace(request, isbn: int, photo_id: int):
    return delete_photo(request, isbn, photo_id, "dedicaces")

def delete_exlibris(request, isbn: int, photo_id: int):
    return delete_photo(request, isbn, photo_id, "exlibris")

def upload_photo(request, isbn: int, photo_type: str):
    if request.method == 'POST':
        auth_header = request.headers.get('Authorization')
        if auth_header is None or auth_header != f"Bearer {POST_TOKEN}":
            return JsonResponse({'error': "Vous n'avez pas l'autorisation"})
        else:
            if 'file' in request.FILES:
                uploaded_file = request.FILES['file']
                service = UploadPhotoService()
                if service.main(isbn, uploaded_file, photo_type):
                    return JsonResponse({'message': f'Fichier {isbn} ajouté avec succès'})
                else:
                    return JsonResponse({'error': "Le type du fichier est incorrect"})
            else:
                return JsonResponse({'error': "Aucun fichier n'a été envoyé"})
    else:
        return JsonResponse({'message': 'Il faut une requête POST'})

def delete_photo(request, isbn: int, photo_id: int, photo_type: str):
    if request.method == 'GET':
        auth_header = request.headers.get('Authorization')
        if auth_header is None or auth_header != f"Bearer {POST_TOKEN}":
            return JsonResponse({'error': "Vous n'avez pas l'autorisation"})
        else:
            service = DeletePhotoService()
            if service.main(isbn, photo_id, photo_type):
                return JsonResponse({'message': 'Photo supprimée correctement'})
            else:
                return JsonResponse({'message': "La photo n'a pas été trouvée"})
    else:
        return JsonResponse({'message': 'Il faut une requête POST'})
