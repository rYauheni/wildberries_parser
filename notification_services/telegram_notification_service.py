import os
import time

import requests

from dotenv import load_dotenv

from exceptions.exceptions import NotificationError
from notification_services.notification_service import NotificationService

load_dotenv()


class TelegramNotificationService(NotificationService):
    def __init__(self):
        self.token = os.environ.get('TOKEN')
        self.chat_id = os.environ.get('CHAT_ID')

    def send_message(self, message):
        try:
            url = f'https://api.telegram.org/bot{self.token}/sendMessage'
            params = {'chat_id': self.chat_id, 'text': message}
            response = requests.post(url, params=params)
            if response.status_code == 429:
                # The Telegram API has a limit on the number of messages sent (status_code=429).
                # If this limit is exceeded, Telegram does not allow sending messages for 40 seconds.
                time.sleep(41)
                requests.post(url, params=params)
            if response.status_code not in (200, 429):
                raise NotificationError(response.status_code)
        except Exception:
            raise NotificationError
