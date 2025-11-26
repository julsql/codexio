import os
from typing import Tuple


def count_images_in_directory(directory_path: str, extensions: Tuple[str, ...] = ('.jpeg',)) -> int:
    if not os.path.isdir(directory_path):
        return 0

    image_count = 0
    for root, _, files in os.walk(directory_path):
        for file in files:
            if os.path.splitext(file)[1].lower() in extensions:
                image_count += 1

    return image_count
