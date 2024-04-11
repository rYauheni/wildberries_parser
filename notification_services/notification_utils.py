from exceptions.error_messages import PRODUCT_DATA_NOT_FOUND_MESSAGE, FEEDBACK_DATA_NOT_FOUND_MESSAGE, EXCEPTION_MESSAGE
from exceptions.exceptions import NotificationError, ProductDataError, FeedbackDataError
from logger_utils.logger_utils import logger
from models.message import Message, MessagesList
from models.product import Product
from notification_services.notification_manager import NotificationManager
from notification_services.notification_messages import create_not_found_negative_feedbacks_message, fill_messages_list
from archive.parser import get_product_data


def send_message(message: Message, pid: int, notification_manager: NotificationManager):
    try:
        notification_manager.send_message(message=message.text)
        logger.info(f'Product {pid}. Message was sent successfully.')
    except NotificationError:
        logger.error(f'ERROR. Product {pid}. Message did not be sent.')


def send_messages(messages_list: MessagesList, product: Product, notification_manager: NotificationManager):
    messages_list = messages_list.messages_list
    if messages_list:
        for message in messages_list:
            send_message(message=message, pid=product.id, notification_manager=notification_manager)

    else:
        message = create_not_found_negative_feedbacks_message(product=product)
        send_message(message, pid=product.id, notification_manager=notification_manager)


def create_messages_list(product: Product, notification_manager: NotificationManager) -> list:
    messages_list = []
    try:
        get_product_data(product=product)
        messages_list = fill_messages_list(product=product, messages_list=messages_list)
        logger.info(f'Product {product.id} has been parsed.')
    except ProductDataError:
        notification_manager.send_message(message=PRODUCT_DATA_NOT_FOUND_MESSAGE)
        logger.error(f'ERROR. Product {product.id} data not found or could not be parsed.')
    except FeedbackDataError:
        notification_manager.send_message(message=FEEDBACK_DATA_NOT_FOUND_MESSAGE)
        logger.error(f'ERROR. Product {product.id} feedback data not found or could not be parsed.')
    except Exception as e:
        notification_manager.send_message(message=EXCEPTION_MESSAGE)
        logger.error(f'ERROR. Product {product.id} raised exception {e}.')

    return messages_list
