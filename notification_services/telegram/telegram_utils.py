import os
import time
from functools import wraps

from dotenv import load_dotenv
import requests

from exceptions.exceptions import NotificationError
from logger_utils.logger_utils import logger


load_dotenv()


def handle_rate_limit(retries: int = 3, delay: int = 40):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries_left = retries
            while retries_left > 0:
                try:
                    response = func(*args, **kwargs)
                    if response.status_code == 429:
                        logger.warning('Rate limited. Waiting 40 seconds before retrying...')
                        time.sleep(delay)
                        retries_left -= 1
                    elif response.status_code != 200:
                        raise NotificationError(response.status_code)
                    else:
                        logger.info('Message was sent successfully.')
                        return response
                except Exception as e:
                    print(e)
                    raise NotificationError("Exceeded maximum retries")
        return wrapper
    return decorator


@handle_rate_limit(retries=3, delay=40)
def telegram_send_message(message: str):
    token = os.environ.get('TOKEN')
    chat_id = os.environ.get('CHAT_ID')
    try:
        url = f'https://api.telegram.org/bot{token}/sendMessage'
        params = {'chat_id': chat_id, 'text': message}
        return requests.post(url, params=params)
    except Exception:
        raise NotificationError
