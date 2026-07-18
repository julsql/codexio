import os


def secure_media_path(base_folder: str, *subpaths: str) -> str:
    """Construit un chemin en garantissant qu'il reste contenu dans base_folder.

    Empêche les attaques de traversée de répertoire (path injection) : le chemin
    résolu (realpath) doit rester à l'intérieur du répertoire de base autorisé,
    sinon une ValueError est levée.
    """
    base_real = os.path.realpath(base_folder)
    candidate = os.path.realpath(os.path.join(base_real, *subpaths))
    if candidate != base_real and not candidate.startswith(base_real + os.sep):
        raise ValueError("Chemin non autorisé")
    return candidate
