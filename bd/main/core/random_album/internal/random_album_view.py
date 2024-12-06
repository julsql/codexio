from typing import Dict

from main.core.random_album.random_album_service import RandomAlbumService


def random_album() -> Dict[str, str]:
    service = RandomAlbumService()
    return service.main()
