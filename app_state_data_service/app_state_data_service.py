from abc import ABC, abstractmethod


class AppStateDataService(ABC):
    @abstractmethod
    def create_app_state_data(self):
        pass

    @abstractmethod
    def set_product_data(self, pid: int, last_update: float):
        pass

    @abstractmethod
    def get_product_data(self, pid: int) -> str:
        pass

    @abstractmethod
    def update_product_data(self, pid: int, last_update: float):
        pass

    @staticmethod
    @abstractmethod
    def create_default_last_update() -> str:
        pass
