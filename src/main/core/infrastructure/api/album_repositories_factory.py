from main.core.domain.model.profile_type import ProfileType
from main.core.domain.ports.repositories.add_album_repository import AddAlbumRepository
from main.core.domain.ports.repositories.album_cache_repository import AlbumCacheRepository
from main.core.domain.ports.repositories.logger_repository import LoggerRepository
from main.core.infrastructure.api.bd_fugue_adapter import BdFugueAdapter
from main.core.infrastructure.api.bd_gest_adapter import BdGestAdapter
from main.core.infrastructure.api.bd_google_adapter import BdGoogleAdapter
from main.core.infrastructure.api.bd_phile_adapter import BdPhileAdapter
from main.core.infrastructure.api.bnf_adapter import BnfAdapter
from main.core.infrastructure.api.cached_album_repository import CachedAlbumRepository
from main.core.infrastructure.api.book_adapter import BookAdapter
from main.core.infrastructure.api.open_library_adapter import OpenLibraryAdapter

# Sources interrogées pour chaque profil, dans l'ordre de priorité de la fusion
SOURCES_BY_PROFILE = {
    ProfileType.BD: {
        "bdphile": BdPhileAdapter,
        "bdgest": BdGestAdapter,
        "bdfugue": BdFugueAdapter,
        "bdgoogle": BdGoogleAdapter,
    },
    ProfileType.BOOK: {
        "googlebooks": BookAdapter,
        "bnf": BnfAdapter,
        "openlibrary": OpenLibraryAdapter,
    },
}

# Sources interrogeables une à une (?source=) mais écartées de la fusion par défaut :
# Cloudflare challenge bdfugue.com depuis le serveur, chaque ajout ferait un appel voué à l'échec
ON_DEMAND_SOURCES = {"bdfugue"}


def available_sources(profile_type: ProfileType) -> list[str]:
    """Noms des sources interrogeables pour un type de profil"""
    return list(SOURCES_BY_PROFILE.get(profile_type, {}))


def build_album_repositories(profile_type: ProfileType,
                             logger_repository: LoggerRepository,
                             source: str | None = None,
                             cache_repository: AlbumCacheRepository | None = None) -> list[AddAlbumRepository]:
    """Construit les repositories d'API externes à interroger pour un type de profil

    Sans source, toutes celles du profil sont renvoyées dans l'ordre de fusion, sauf ON_DEMAND_SOURCES.
    Avec une source, seule celle-ci est renvoyée ; un nom inconnu renvoie une liste vide.
    Avec un cache, chaque source est enveloppée pour ne pas être réinterrogée inutilement.
    """
    adapters = SOURCES_BY_PROFILE.get(profile_type, {})

    if source is not None:
        adapter = adapters.get(source)
        if not adapter:
            return []
        selected = [adapter]
    else:
        selected = [adapter for name, adapter in adapters.items() if name not in ON_DEMAND_SOURCES]

    repositories = [adapter(logger_repository) for adapter in selected]

    if cache_repository is None:
        return repositories

    return [CachedAlbumRepository(repository, cache_repository) for repository in repositories]
