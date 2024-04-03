from abc import ABC, abstractmethod


class NotificationStorage(ABC):
    @abstractmethod
    def send_message(self, message):
        pass
