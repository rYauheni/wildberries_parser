from app_state_data_service.json_app_state_data_service import JSONAppStateDataService
from exceptions.exceptions import NotificationError
from models.message import MessagesList, MessagesSender
from notification_services.notification_manager import NotificationManager
from notification_services.telegram.telegram_notification_service import TelegramNotificationService
from parser.product_parser import create_product
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

        product = create_product(pid=pid, product_last_update=last_update)

        messages_list = MessagesList(product=product)
        messages_list.fill_messages_list()

        messages_sender = MessagesSender(messages_list=messages_list)

        try:
            messages_sender.handle_messages_sender(notification_manager=notification_manager)
        except NotificationError:
            pass
        else:
            app_state_service.update_product_data(pid=product.id, last_update=product.last_update)


if __name__ == '__main__':
    main()
