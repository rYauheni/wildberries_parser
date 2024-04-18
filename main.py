from app_state_data_service.json_app_state_data_service import JSONAppStateDataService
from exceptions.exceptions import ProductDataError, FeedbackDataError, NotificationError
from logger_utils.logger_utils import logger
from models.message import MessagesList
from models.product import Product, Status
from notification_services.notification_manager import NotificationManager
from notification_services.telegram_notification_service import TelegramNotificationService
from product_id_access_services.excel_product_id_access_service import ExcelProductIDAccessService
from product_id_access_services.product_id_access_utils import get_products_ids


def main():
    app_state_service = JSONAppStateDataService()

    notification_services = (TelegramNotificationService(),)
    notification_manager = NotificationManager()
    notification_manager.add_services(services=notification_services)

    product_id_access_service = ExcelProductIDAccessService()

    app_state_service.create_app_state_data()
    products_ids = get_products_ids(prodict_service=product_id_access_service,
                                    notification_manager=notification_manager)
    default_last_update = app_state_service.set_default_last_update()
    for pid in products_ids:
        product = Product(id=pid)

        if not app_state_service.get_app_state_data(pid=product.id):
            app_state_service.set_app_state_data(pid=product.id, last_update=default_last_update)
        product.last_update = app_state_service.get_app_state_data(pid=product.id)

        try:
            product.parse_product_data()
            logger.info(f'Product {product.id} has been parsed.')
        except ProductDataError:
            product.status = Status.PRODUCT_DNF
            logger.error(f'Product {product.id} data not found or could not be parsed.')
        except FeedbackDataError:
            product.status = Status.FEEDBACK_DNF
            logger.error(f'Product {product.id} feedback data not found or could not be parsed.')
        except Exception as e:
            product.status = Status.UNKNOWN_E
            logger.error(f'Product {product.id} raised exception {e}.')

        messages_list = MessagesList(product=product)
        messages_list.fill_messages_list()

        try:
            messages_list.send_messages(notification_manager=notification_manager)
            logger.info(f'Product {product.id}. Messages ware sent successfully.')
        except NotificationError:
            logger.error(f'Product {product.id}. Messages did not be sent.')
        else:
            app_state_service.update_app_state_data(pid=product.id,
                                                    last_update=product.last_update)


if __name__ == '__main__':
    main()
