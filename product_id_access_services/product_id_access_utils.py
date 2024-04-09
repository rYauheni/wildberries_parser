import logging

from exceptions.error_messages import IDS_NOT_FOUND, FILE_NOT_FOUND_MESSAGE
from exceptions.exceptions import FileError
from notification_services.notification_manager import NotificationManager
from product_id_access_services.excel_product_id_access_service import ExcelProductIDAccessService

# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
# )
# logger = logging.getLogger(__name__)

from logger_utils.logger_utils import logger


def get_products_ids(prodict_service: ExcelProductIDAccessService, notification_manager: NotificationManager) -> list:
    products_ids = []
    try:
        products_ids = prodict_service.get_ids()
        logger.info(f'Extract ids from {prodict_service.source}.')
    except FileError:
        notification_manager.send_message(message=FILE_NOT_FOUND_MESSAGE)
        logger.error(f'ERROR. File {prodict_service.source} not found or the file could not be parsed.')

    if not products_ids:
        notification_manager.send_message(message=IDS_NOT_FOUND)
        logger.error(f'No ids found in the file {prodict_service.source}.')
    return products_ids
