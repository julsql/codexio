from typing import Dict

from main.core.banner.banner_service import RandomDedicaceService


def random_dedicace() -> Dict[str, str]:
    service = RandomDedicaceService()
    return service.main()
