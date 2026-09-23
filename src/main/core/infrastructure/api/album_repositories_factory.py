from main.core.domain.model.profile_type import ProfileType
from main.core.domain.ports.repositories.add_album_repository import AddAlbumRepository
from main.core.domain.ports.repositories.logger_repository import LoggerRepository
from main.core.infrastructure.api.bd_fugue_adapter import BdFugueAdapter
from main.core.infrastructure.api.bd_gest_adapter import BdGestAdapter
from main.core.infrastructure.api.bd_google_adapter import BdGoogleAdapter
from main.core.infrastructure.api.bd_phile_adapter import BdPhileAdapter
from main.core.infrastructure.api.bnf_adapter import BnfAdapter
from main.core.infrastructure.api.book_adapter import BookAdapter
from main.core.infrastructure.api.open_library_adapter import OpenLibraryAdapter


def build_album_repositories(profile_type: ProfileType,
                             logger_repository: LoggerRepository) -> list[AddAlbumRepository]:
    """Construit la liste des repositories d'API externes à interroger pour un type de profil"""
    if profile_type == ProfileType.BD:
        return [
            BdPhileAdapter(logger_repository),
            BdGestAdapter(logger_repository),
            BdFugueAdapter(logger_repository),
            BdGoogleAdapter(logger_repository),
        ]
    elif profile_type == ProfileType.BOOK:
        return [
            BookAdapter(logger_repository),
            BnfAdapter(logger_repository),
            OpenLibraryAdapter(logger_repository),
        ]
    return []
