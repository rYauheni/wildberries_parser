from abc import ABC, abstractmethod


class NotificationService(ABC):
    @abstractmethod
    def send_message(self, message):
        pass
