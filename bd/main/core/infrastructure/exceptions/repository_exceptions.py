class InfrastructureException(Exception):
    """Exception de base pour l'infrastructure"""
    pass


class RepositoryException(InfrastructureException):
    """Exception liée aux repositories"""
    pass


class ConnectionException(InfrastructureException):
    """Exception de connexion"""
    pass


class ExternalServiceException(InfrastructureException):
    """Exception pour les services externes (API, etc.)"""
    pass
