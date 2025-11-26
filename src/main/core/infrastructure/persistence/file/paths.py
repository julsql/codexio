import os

from config.settings import MEDIA_ROOT

IMAGE_ROOT = "main/images"


def SIGNED_COPY_PATH(collection_id: int):
    return f"{IMAGE_ROOT}/{collection_id}/dedicaces"


def EXLIBRIS_PATH(collection_id: int):
    return f"{IMAGE_ROOT}/{collection_id}/exlibris"


def SIGNED_COPY_FOLDER(collection_id: int):
    return os.path.join(MEDIA_ROOT, SIGNED_COPY_PATH(collection_id))


def EXLIBRIS_FOLDER(collection_id: int):
    return os.path.join(MEDIA_ROOT, EXLIBRIS_PATH(collection_id))
