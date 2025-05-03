from abc import ABC, abstractmethod


class BannerRepository(ABC):

    @abstractmethod
    def get_all_images_path(self, paths: list[str]) -> list[str]:
        pass

    @abstractmethod
    def get_random_attachment(self, images_files: list[str]) -> tuple[str, str, str]:
        pass
