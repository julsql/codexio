import os
import re

from config.settings import STATIC_ROOT
from django.core.files.storage import FileSystemStorage

class UploadPhotoService:
    def __init__(self):
        self.allowed_extensions = '.jpeg'
        self.dedicace_folder = os.path.join(STATIC_ROOT, 'main/images/dedicaces')
        self.exlibris_folder = os.path.join(STATIC_ROOT, 'main/images/exlibris')

    def main(self, isbn: int, uploaded_file, photo_type: str) -> bool:
        if photo_type == 'dedicaces':
            origin_folder = self.dedicace_folder
        else:
            origin_folder = self.exlibris_folder

        allowed_file = self.is_allowed_file(uploaded_file.name)
        if allowed_file:
            file_extension = os.path.splitext(uploaded_file.name)[1].lower()
            path_folder = os.path.join(origin_folder, str(isbn))
            number = self.get_next_number(path_folder)
            fs = FileSystemStorage(location=path_folder)

            fs.save(f"{number}{file_extension}", uploaded_file)
        return allowed_file

    def is_allowed_file(self, filename: str) -> bool:
        return '.' in filename and "." + filename.rsplit('.', 1)[1].lower() == self.allowed_extensions

    def get_next_number(self, directory_path):
        if not os.path.isdir(directory_path):
            return 1

        image_paths = []
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_extension = os.path.splitext(file)[1].lower()
                if file_extension == self.allowed_extensions:
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
