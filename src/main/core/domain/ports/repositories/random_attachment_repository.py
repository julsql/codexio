from abc import ABC, abstractmethod

from main.core.domain.model.random_attachment import RandomAttachment


class RandomAttachmentRepository(ABC):

    @abstractmethod
    def get_all_images_path(self, paths: list[str]) -> list[str]:
        pass

    @abstractmethod
    def get_random_attachment(self, images_files: list[str]) -> RandomAttachment:
        pass
