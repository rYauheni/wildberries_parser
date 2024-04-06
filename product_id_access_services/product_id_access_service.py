from abc import ABC, abstractmethod


class ProductIDAccessService(ABC):
    @abstractmethod
    def get_ids(self):
        pass
