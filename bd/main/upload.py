import os
import re
import json

from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from bd.settings import POST_TOKEN

ALLOWED_EXTENSIONS = 'jpeg'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == ALLOWED_EXTENSIONS


def upload_dedicace(request, isbn):
    __FILEPATH__ = (os.path.dirname(os.path.abspath(__file__)))
    DEDICACE_FOLDER = os.path.join(__FILEPATH__, 'static/main/images/dedicaces')
    return upload(request, isbn, DEDICACE_FOLDER)


def upload_exlibris(request, isbn):
    __FILEPATH__ = os.path.dirname(os.path.abspath(__file__))
    EXLIBRIS_FOLDER = os.path.join(__FILEPATH__, 'static/main/images/exlibris')
    return upload(request, isbn, EXLIBRIS_FOLDER)


def upload(request, isbn, origin_folder):
    if request.method == 'POST':
        if 'token' not in request.POST or request.POST['token'] != f"Bearer {POST_TOKEN}":
            return JsonResponse({'error': "You don't have the authorization"})
        else:
            if 'file' in request.FILES:
                uploaded_file = request.FILES['file']
                if allowed_file(uploaded_file.name):
                    file_extension = os.path.splitext(uploaded_file.name)[1].lower()
                    path_folder = os.path.join(origin_folder, str(isbn))
                    number = get_next_number(path_folder)

                    fs = FileSystemStorage(location=path_folder)

                    fs.save(f"{number}{file_extension}", uploaded_file)
                    return JsonResponse({'message': 'File uploaded successfully'})
                else:
                    return JsonResponse({'error': 'File type not allowed'})
            else:
                return JsonResponse({'error': 'No file part or no selected file'})
    else:
        return JsonResponse({'message': 'Please make a POST request'})




def get_next_number(directory_path):
    if not os.path.isdir(directory_path):
        return 1

    image_paths = []
    allowed_image_extensions = ".jpeg"

    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_extension = os.path.splitext(file)[1].lower()
            if file_extension == allowed_image_extensions:
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
