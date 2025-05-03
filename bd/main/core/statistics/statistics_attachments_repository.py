from abc import ABC, abstractmethod


class StatisticsAttachmentsRepository(ABC):
    @abstractmethod
    def get_information(self):
        pass
