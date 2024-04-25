from exceptions.exceptions import NotificationError
from notification_services.notification_service import NotificationService
from notification_services.telegram.telegram_utils import telegram_send_message


class TelegramNotificationService(NotificationService):

    def send_message(self, message: str):
        try:
            telegram_send_message(message=message)
        except NotificationError:
            raise
