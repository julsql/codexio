from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from config.settings import POST_TOKEN
from main.core.delete_photo.delete_photo_service import DeletePhotoService

@csrf_exempt
def delete_dedicace(request, isbn: int, photo_id: int):
    return delete_photo(request, isbn, photo_id, "dedicaces")

@csrf_exempt
def delete_exlibris(request, isbn: int, photo_id: int):
    return delete_photo(request, isbn, photo_id, "exlibris")

def delete_photo(request, isbn: int, photo_id: int, photo_type: str):
    if request.method == 'DELETE':
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
        return JsonResponse({'message': 'Il faut une requête DELETE'})
