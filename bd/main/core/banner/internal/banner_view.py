from main.core.banner.banner_service import BannerService
from main.core.banner.internal.banner_connexion import BannerConnexion


def random_attachment() -> dict[str, str]:
    repository = BannerConnexion()
    service = BannerService(repository)
    return service.main()
