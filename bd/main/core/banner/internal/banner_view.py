from main.core.banner.banner_service import RandomDedicaceService


def random_dedicace() -> dict[str, str]:
    service = RandomDedicaceService()
    return service.main()
