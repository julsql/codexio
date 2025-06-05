import os

from config.settings import MEDIA_ROOT

SIGNED_COPY_PATH = "main/images/dedicaces"
EXLIBRIS_PATH = "main/images/exlibris"

SIGNED_COPY_FOLDER = os.path.join(MEDIA_ROOT, SIGNED_COPY_PATH)
EXLIBRIS_FOLDER = os.path.join(MEDIA_ROOT, EXLIBRIS_PATH)
