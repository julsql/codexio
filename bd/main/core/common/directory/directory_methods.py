import os


def count_images_in_directory(directory_path: str) -> int:
    if not os.path.isdir(directory_path):
        return 0

    image_count = 0
    allowed_image_extensions = ".jpeg"

    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_extension = os.path.splitext(file)[1].lower()
            if file_extension == allowed_image_extensions:
                image_count += 1

    return image_count
