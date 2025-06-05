from main.domain.exceptions.domain_exceptions import DomainException


class ApiException(DomainException):
    """Exception de base pour les APIs"""

    def __init__(self, message: str, website: str, isbn: int = None):
        if isbn:
            message = f"Site {website} (ISBN {isbn}) : {message}"
        else:
            message = f"Site {website} : {message}"
        super().__init__(message)


class ApiConnexionDataNotFound(ApiException):
    """Data non trouvée sur l'API"""
    pass


class ApiConnexionException(ApiException):
    """API non accessible"""
    pass


class ApiConnexionRefused(ApiException):
    """Mauvais token d'API"""
    pass
