from abc import ABC, abstractmethod


class ProductIDExtractService(ABC):
    @abstractmethod
    def get_ids(self):
        pass
