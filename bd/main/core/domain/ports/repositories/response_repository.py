from abc import ABC, abstractmethod
from typing import Any, Optional, Sequence


class ResponseRepository(ABC):
    @abstractmethod
    def success(self, content: str, status: int = 200) -> Any:
        """Crée une réponse réussie"""
        pass

    @abstractmethod
    def forbidden(self, content: str) -> Any:
        """Crée une réponse interdite"""
        pass

    @abstractmethod
    def not_found(self, content: str) -> Any:
        """Crée une réponse non trouvée"""
        pass

    @abstractmethod
    def method_not_allowed(self, permitted_methods: Sequence[str], content: Optional[str] = None) -> Any:
        """Crée une réponse méthode non autorisée"""
        pass

    @abstractmethod
    def bad_request(self, content: str) -> Any:
        """Crée une réponse requête invalide"""
        pass

    @abstractmethod
    def server_error(self, content: str) -> Any:
        """Crée une réponse erreur serveur"""
        pass

    @abstractmethod
    def technical_error(self, content: str) -> Any:
        """Crée une réponse erreur serveur technique"""
        pass
