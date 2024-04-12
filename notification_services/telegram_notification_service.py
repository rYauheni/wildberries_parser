import os
import time

import requests

from dotenv import load_dotenv

from exceptions.exceptions import NotificationError
from logger_utils.logger_utils import logger
from models.message import Message
from notification_services.notification_service import NotificationService

load_dotenv()


class TelegramNotificationService(NotificationService):
    def __init__(self):
        self.token = os.environ.get('TOKEN')
        self.chat_id = os.environ.get('CHAT_ID')

    def send_message(self, message: str, retries: int = 3):
        try:
            url = f'https://api.telegram.org/bot{self.token}/sendMessage'
            params = {'chat_id': self.chat_id, 'text': message}
            response = requests.post(url, params=params)
            if response.status_code == 429:

                # The Telegram API has a limit on the number of messages sent (status_code=429).
                # If this limit is exceeded, Telegram does not allow sending messages for 40 seconds.
                logger.warning('Rate limited. Waiting 40 seconds before retrying...')
                time.sleep(40)
                if retries > 1:
                    self.send_message(message, retries=retries - 1)
                else:
                    raise NotificationError("Exceeded maximum retries")
            elif response.status_code != 200:
                raise NotificationError(response.status_code)
            else:
                logger.info('Message was sent successfully.')
        except Exception:
            raise NotificationError
