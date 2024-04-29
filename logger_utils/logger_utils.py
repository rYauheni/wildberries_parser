import inspect
import logging
import os
import time
from enum import Enum

import requests
from dotenv import load_dotenv

import exceptions.error_messages as em
# from notification_services.telegram.telegram_notification_service import TelegramNotificationService


class CustomFormatter(logging.Formatter):
    COLORS = {'DEBUG': '\033[94m', 'INFO': '\033[92m', 'WARNING': '\033[93m', 'ERROR': '\033[91m',
              'CRITICAL': '\033[95m'}

    def format(self, record):
        color = self.COLORS.get(record.levelname, '')
        log_fmt = f"{color}%(asctime)s - {color}%(filename)s - {color}%(levelname)s - {color}%(message)s\033[0m"
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class CustomHandler(logging.StreamHandler):

    def handle(self, record):
        # Signal template: logger.info('msg', extra={'signal': Signal.SMTH})
        if hasattr(record, 'signal'):
            message = SignalToMessageConverter().convert(signal=record.signal)
            self.notify(message=message)

        if record.levelno == logging.CRITICAL:
            with open('critical.log', 'a') as file:
                log_entry = f'{record.asctime} - {record.filename} - {record.message}'
                file.write(log_entry + '\n')

    @staticmethod
    def notify(message):
        # DRY DISTURBER
        load_dotenv()
        token = os.environ.get('TOKEN')
        chat_id = os.environ.get('CHAT_ID')
        url = f'https://api.telegram.org/bot{token}/sendMessage'
        params = {'chat_id': chat_id, 'text': message}
        requests.post(url, params=params)

        # notification_service = TelegramNotificationService()
        # notification_service.send_message(message=message)


class Signal(Enum):
    SOURCE_NOT_FOUND = 'source_not_found'
    IDS_NOT_FOUND = 'ids_not_found'
    ROOT_NOT_FOUND = 'root_not_found'
    PRODUCT_DATA_NOT_FOUND = 'product_data_not_found'
    FEEDBACK_DATA_NOT_FOUND = 'feedback_data_not_found'
    EXCEPTION = 'exception'


class SignalToMessageConverter:
    @staticmethod
    def convert(signal: Signal) -> str:
        message = ''
        match signal:
            case Signal.SOURCE_NOT_FOUND:
                message = em.SOURCE_NOT_FOUND_MESSAGE
            case Signal.IDS_NOT_FOUND:
                message = em.IDS_NOT_FOUND
            # case Signal.ROOT_NOT_FOUND:
            #     message = em.ROOT_NOT_FOUND_MESSAGE
            # case Signal.PRODUCT_DATA_NOT_FOUND:
            #     message = em.PRODUCT_DATA_NOT_FOUND_MESSAGE
            # case Signal.FEEDBACK_DATA_NOT_FOUND:
            #     message = em.FEEDBACK_DATA_NOT_FOUND_MESSAGE
            # case Signal.EXCEPTION:
            #     message = em.EXCEPTION_MESSAGE
        return message


logging.basicConfig(
    level=logging.DEBUG,
)
logging.getLogger().handlers[0].setFormatter(CustomFormatter())

logger = logging.getLogger()
logger.addHandler(CustomHandler())
