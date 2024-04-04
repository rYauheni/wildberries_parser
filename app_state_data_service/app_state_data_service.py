from abc import ABC, abstractmethod


class AppStateDataService(ABC):
    @abstractmethod
    def create_app_state_data(self):
        pass

    @abstractmethod
    def set_app_state_data(self, pid: int, last_update: str):
        pass

    @abstractmethod
    def get_app_state_data(self, pid: int) -> str:
        pass

    @abstractmethod
    def update_app_state_data(self, pid: int, last_update: str):
        pass

    @staticmethod
    @abstractmethod
    def set_default_last_update() -> str:
        pass
