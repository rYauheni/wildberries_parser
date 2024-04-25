import os
import time

import requests

from dotenv import load_dotenv

from exceptions.exceptions import NotificationError
from logger_utils.logger_utils import logger
from models.message import Message
from notification_services.notification_service import NotificationService
from notification_services.telegram.telegram_utils import telegram_send_message

load_dotenv()


class TelegramNotificationService(NotificationService):
    def __init__(self):
        self.token = os.environ.get('TOKEN')
        self.chat_id = os.environ.get('CHAT_ID')

    def send_message(self, message: str):
        try:
            telegram_send_message(token=self.token, chat_id=self.chat_id, message=message)
        except NotificationError:
            raise
