from typing import Dict

from main.core.random_dedicace.random_dedicace_service import RandomDedicaceService


def random_dedicace() -> Dict[str, str]:
    service = RandomDedicaceService()
    return service.main()
