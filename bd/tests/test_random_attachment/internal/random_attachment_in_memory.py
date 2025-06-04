from main.domain.model.random_attachment import RandomAttachment
from main.domain.ports.repositories.random_attachment_repository import RandomAttachmentRepository


class RandomAttachmentInMemory(RandomAttachmentRepository):
    def __init__(self):
        self.images = []
        self.get_all_images_path_called = False
        self.get_random_attachment_called = False
        self.last_paths_param = None
        self.last_images_param = None
        self.return_random_attachment = None

    def get_all_images_path(self, paths: list[str]) -> list[str]:
        self.get_all_images_path_called = True
        self.last_paths_param = paths
        return self.images

    def get_random_attachment(self, images_files: list[str]) -> RandomAttachment:
        self.get_random_attachment_called = True
        self.last_images_param = images_files
        return self.return_random_attachment if self.return_random_attachment else (
            RandomAttachment(path="", isbn=0,type=None))
