from main.core.banner.banner_repository import BannerRepository


class BannerInMemory(BannerRepository):
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

    def get_random_attachment(self, images_files: list[str]) -> tuple[str, str, str]:
        self.get_random_attachment_called = True
        self.last_images_param = images_files
        return self.return_random_attachment if self.return_random_attachment else ("", 0, "")
