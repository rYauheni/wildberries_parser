from app_state_data_service.json_app_state_data_service import JSONAppStateDataService
from logger_utils.logger_utils import logger
from models.message import MessagesList
from models.product import Product, Status
from notification_services.notification_manager import NotificationManager
from notification_services.telegram_notification_service import TelegramNotificationService
from product_id_extract_services.excel_product_id_extract_service import ExcelProductIDExtractService
from product_id_extract_services.product_id_extract_utils import get_products_ids


def main():
    app_state_service = JSONAppStateDataService()

    notification_services = [TelegramNotificationService()]
    notification_manager = NotificationManager(services=notification_services)

    product_id_extract_service = ExcelProductIDExtractService()

    app_state_service.create_app_state_data()
    products_ids = get_products_ids(product_service=product_id_extract_service,
                                    notification_manager=notification_manager)
    default_last_update = app_state_service.create_default_last_update()
    for pid in products_ids:
        product = Product(id=pid)

        if not app_state_service.get_product_data(pid=product.id):
            app_state_service.set_product_data(pid=product.id, last_update=default_last_update)
        product.last_update = app_state_service.get_product_data(pid=product.id)

        product.handle_product_data_parser()

        messages_list = MessagesList(product=product)
        messages_list.fill_messages_list()
        messages_list.handle_messages_sender(notification_manager=notification_manager,
                                             app_state_service=app_state_service)


if __name__ == '__main__':
    main()
