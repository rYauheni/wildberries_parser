from exceptions.error_messages import IDS_NOT_FOUND, FILE_NOT_FOUND_MESSAGE
from exceptions.exceptions import FileError
from logger_utils.logger_utils import logger
from notification_services.notification_manager import NotificationManager
from product_id_extract_services.excel_product_id_extract_service import ExcelProductIDExtractService


def get_products_ids(product_service: ExcelProductIDExtractService, notification_manager: NotificationManager) -> list:
    products_ids = []
    try:
        products_ids = product_service.get_ids()
        logger.info(f'Extract ids from {product_service.source}.')
    except FileError:
        notification_manager.send_message(message=FILE_NOT_FOUND_MESSAGE)
        logger.error(f'ERROR. Source {product_service.source} not found or the source could not be parsed.')
    else:
        if not products_ids:
            notification_manager.send_message(message=IDS_NOT_FOUND)
            logger.error(f'No ids found in the source {product_service.source}.')
    return products_ids