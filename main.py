from app_state_data_service.json_app_state_data_service import JSONAppStateDataService
from logger_utils.logger_utils import logger
from models.message import MessagesList
from models.product import Product, Status
from notification_services.notification_manager import NotificationManager
from notification_services.telegram_notification_service import TelegramNotificationService
from parser.product_parser import ProductParser
from product_id_extract_services.excel_product_id_extract_service import ExcelProductIDExtractService
from product_id_extract_services.file_provider import FileProvider
from product_id_extract_services.product_id_extract_utils import get_products_ids


def main():
    app_state_service = JSONAppStateDataService()

    notification_services = [TelegramNotificationService()]
    notification_manager = NotificationManager(services=notification_services)

    file_path = FileProvider().get_file_path()
    product_id_extract_service = ExcelProductIDExtractService(excel_file_path=file_path)

    app_state_service.create_app_state_data()
    products_ids = get_products_ids(product_service=product_id_extract_service)
    default_last_update = app_state_service.create_default_last_update()
    for pid in products_ids:

        if not app_state_service.get_product_data(pid=pid):
            app_state_service.set_product_data(pid=pid, last_update=default_last_update)
        last_update = float(app_state_service.get_product_data(pid=pid))



        product_parser = ProductParser(pid=pid, last_update=last_update)
        product = Product(
            id=pid,
            url=product_parser.product_url,
            root=product_parser.product_root_from_json(),
            name=product_parser.product_name_from_json(),
            rating=product_parser.product_rating_from_json(),
            feedbacks=product_parser.parse_product_feedbacks(),
            last_update=product_parser.product_last_update # last_update must necessarily come after feedbacks, otherwise there is a violation of logic and incorrect data
        )

        # product.handle_product_data_parser() TODO

        messages_list = MessagesList(product=product)
        messages_list.fill_messages_list()
        messages_list.handle_messages_sender(notification_manager=notification_manager,
                                             app_state_service=app_state_service)


if __name__ == '__main__':
    main()
