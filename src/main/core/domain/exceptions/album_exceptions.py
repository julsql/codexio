from main.core.domain.exceptions.domain_exceptions import DomainException


class AlbumException(DomainException):
    """Exception de base pour les albums"""

    def __init__(self, message: str, isbn: int = None):
        super().__init__(f"ISBN {isbn}: {message}")


class AlbumNotFoundException(AlbumException):
    """Album non trouvé"""
    pass


class AlbumAlreadyExistsException(AlbumException):
    """Album déjà existant"""
    pass


class InvalidAlbumDataException(AlbumException):
    """Données d'album invalides"""
    pass


class AlbumSourcesUnavailableException(AlbumException):
    """Aucune donnée obtenue alors qu'au moins une source a échoué techniquement"""

    def __init__(self, message: str, isbn: int = None, sources: list[str] = None):
        super().__init__(message, isbn)
        self.sources = sources or []
