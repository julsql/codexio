import os
import re
from abc import ABC

from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import UploadedFile

from main.core.update_images.bd_repository import BdRepository


class PhotoConnexion(BdRepository, ABC):

    def __init__(self, dedicace_folder: str, exlibris_folder: str):
        self.allowed_extensions = {'.jpeg'}

        self.dedicace_folder = dedicace_folder
        self.exlibris_folder = exlibris_folder

    def upload_dedicace(self, isbn: int, uploaded_file: UploadedFile) -> bool:
        return self.upload_photo(isbn, uploaded_file, self.dedicace_folder)

    def upload_exlibris(self, isbn: int, uploaded_file: UploadedFile) -> bool:
        return self.upload_photo(isbn, uploaded_file, self.exlibris_folder)

    def upload_photo(self, isbn: int, uploaded_file: UploadedFile, folder: str) -> bool:
        allowed_file = self.is_image_file(uploaded_file.name)
        if allowed_file:
            file_extension = self.get_file_extension(uploaded_file.name)
            path_folder = os.path.join(folder, str(isbn))
            number = self.get_next_number(path_folder)
            fs = FileSystemStorage(location=path_folder)

            fs.save(f"{number}{file_extension}", uploaded_file)
        return allowed_file

    def is_image_file(self, file_path: str) -> bool:
        return os.path.isfile(file_path) and self.get_file_extension(file_path) in self.allowed_extensions

    def get_file_extension(self, file_path: str) -> str:
        return os.path.splitext(file_path)[1].lower()

    def get_next_number(self, directory_path: str) -> int:
        if not os.path.isdir(directory_path):
            return 1

        image_paths = []
        for _, _, files in os.walk(directory_path):
            for file in files:
                file_extension = self.get_file_extension(file)
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
