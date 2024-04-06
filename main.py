import logging

from excel_utils import get_excel_file_path, extract_ids_from_excel
from exceptions.error_messages import (FILE_NOT_FOUND_MESSAGE,
                                       IDS_NOT_FOUND,
                                       PRODUCT_DATA_NOT_FOUND_MESSAGE,
                                       FEEDBACK_DATA_NOT_FOUND_MESSAGE,
                                       EXCEPTION_MESSAGE, )
from exceptions.exceptions import FileError, ProductDataError, FeedbackDataError, NotificationError
from notification_services.notification_manager import NotificationManager
from notification_services.notification_messages import (fill_messages_list,
                                                         create_not_found_negative_feedbacks_message)
from objects.product import Product
from parser import get_product_data
from settings import APP_STATE_SERVICE, NOTIFICATION_SERVICES

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

app_state_service = APP_STATE_SERVICE()

notification_services = [service() for service in NOTIFICATION_SERVICES]

notification_manager = NotificationManager()
notification_manager.add_services(services=notification_services)


def send_message(message: str, pid: int):
    try:
        notification_manager.send_message(message=message)
        logger.info(f'Product {pid}. Message was sent successfully.')
    except NotificationError:
        logger.info(f'ERROR. Product {pid}. Message did not be sent.')


def send_messages(messages_list: list, product: Product):
    if messages_list:
        for message in messages_list:
            send_message(message=message, pid=product.id)

    else:
        message = create_not_found_negative_feedbacks_message(product=product)
        send_message(message, pid=product.id)


def create_messages_list(product) -> list:
    messages_list = []
    try:
        get_product_data(product=product)
        messages_list = fill_messages_list(product=product, messages_list=messages_list)
        logger.info(f'Product {product.id} has been parsed.')
    except ProductDataError:
        notification_manager.send_message(message=PRODUCT_DATA_NOT_FOUND_MESSAGE)
        logger.info(f'ERROR. Product {product.id} data not found or could not be parsed.')
    except FeedbackDataError:
        notification_manager.send_message(message=FEEDBACK_DATA_NOT_FOUND_MESSAGE)
        logger.info(f'ERROR. Product {product.id} feedback data not found or could not be parsed.')
    except Exception as e:
        notification_manager.send_message(message=EXCEPTION_MESSAGE)
        logger.info(f'ERROR. Product {product.id} raised exception {e}.')

    return messages_list


def get_products_ids(file_path: str) -> list:
    products_ids = []
    try:
        products_ids = extract_ids_from_excel(file_path=file_path)
        logger.info(f'Extract ids from {file_path}.')
    except FileError:
        notification_manager.send_message(message=FILE_NOT_FOUND_MESSAGE)
        logger.info(f'ERROR. File {file_path} not found or the file could not be parsed.')

    if not products_ids:
        notification_manager.send_message(message=IDS_NOT_FOUND)
        logger.info(f'No ids found in the file {file_path}.')
    return products_ids


def main():
    app_state_service.create_app_state_data()
    file_path = get_excel_file_path()
    products_ids = get_products_ids(file_path=file_path)
    # default_last_update = app_state_service.set_default_last_update()
    default_last_update = '2024-04-02T13:06:31Z'
    for pid in products_ids:
        product = Product(id=pid)
        if not app_state_service.get_app_state_data(pid=product.id):
            app_state_service.set_app_state_data(pid=product.id, last_update=default_last_update)
        product.last_update = app_state_service.get_app_state_data(pid=product.id)
        messages_list = create_messages_list(product=product)
        app_state_service.update_app_state_data(pid=product.id,
                                                last_update=product.last_update)  # WARNING! Update state data must be after create_messages_list()

        send_messages(messages_list=messages_list, product=product)


if __name__ == '__main__':
    main()
