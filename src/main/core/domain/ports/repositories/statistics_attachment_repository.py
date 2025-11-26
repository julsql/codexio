from abc import ABC, abstractmethod

from main.core.domain.model.statistics import Statistics


class StatisticsAttachmentRepository(ABC):
    @abstractmethod
    def get_attachment_statistics(self) -> Statistics:
        pass
