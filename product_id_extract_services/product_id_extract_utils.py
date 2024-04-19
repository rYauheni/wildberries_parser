from exceptions.error_messages import IDS_NOT_FOUND, FILE_NOT_FOUND_MESSAGE
from exceptions.exceptions import SourceError
from logger_utils.logger_utils import logger
from notification_services.notification_manager import NotificationManager
from product_id_extract_services.excel_product_id_extract_service import ExcelProductIDExtractService
from product_id_extract_services.product_id_extract_service import ProductIDExtractService


def get_products_ids(product_service: ProductIDExtractService, notification_manager: NotificationManager) -> list:
    products_ids = []
    try:
        products_ids = product_service.get_ids()
        logger.info(f'Extract ids:\n\t{"\n\t".join(str(pid) for pid in products_ids)}')
    except SourceError:
        notification_manager.send_message(message=FILE_NOT_FOUND_MESSAGE)
        logger.error(f'ID source not found or the source could not be parsed.')
    else:
        if not products_ids:
            notification_manager.send_message(message=IDS_NOT_FOUND)
            logger.error(f'No ids found in the id source.')
    return products_ids
