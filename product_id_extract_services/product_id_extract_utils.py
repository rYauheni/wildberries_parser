from exceptions.exceptions import SourceError
from logger_utils.logger_utils import logger, Signal
from product_id_extract_services.product_id_extract_service import ProductIDExtractService


def get_products_ids(product_service: ProductIDExtractService) -> list:
    products_ids = []
    try:
        products_ids = product_service.get_ids()
        logger.info(f'Extract ids:\n\t{"\n\t".join(str(pid) for pid in products_ids)}')
    except SourceError:
        logger.error(f'ID source not found or the source could not be parsed.',
                     extra={'signal': Signal.SOURCE_NOT_FOUND})
    else:
        if not products_ids:
            logger.error(f'No ids found in the id source.',
                         extra={'signal': Signal.IDS_NOT_FOUND})
    return products_ids
