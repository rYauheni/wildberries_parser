from notification_services.notification_service import NotificationService


class NotificationManager:
    def __init__(self):
        self.services: list = []

    def add_services(self, services):
        for service in services:
            self.services.append(service)

    def send_message(self, message):
        for service in self.services:
            service.send_message(message=message)
