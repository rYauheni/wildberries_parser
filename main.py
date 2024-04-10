from app_state_data_service.json_app_state_data_service import JSONAppStateDataService
from models.message import MessagesList
from models.product import Product
from notification_services.notification_manager import NotificationManager
from notification_services.notification_utils import create_messages_list, send_messages
from notification_services.telegram_notification_service import TelegramNotificationService
from parser import get_product_data
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
    # default_last_update = app_state_service.set_default_last_update()  # Enable for prod.
    default_last_update = '2024-04-04T13:06:31Z'  # Enable for dev only.
    for pid in products_ids:
        product = Product(id=pid)

        if not app_state_service.get_app_state_data(pid=product.id):
            app_state_service.set_app_state_data(pid=product.id, last_update=default_last_update)
        product.last_update = app_state_service.get_app_state_data(pid=product.id)
        # messages_list = create_messages_list(product=product, notification_manager=notification_manager)

        # get_product_data(product=product)
        product.parse_product_data()

        messages_list = MessagesList(product=product)
        messages_list.fill_messages_list()

        app_state_service.update_app_state_data(pid=product.id,
                                                last_update=product.last_update)  # WARNING! Update state data must be after create_messages_list()

        send_messages(messages_list=messages_list, product=product, notification_manager=notification_manager)


if __name__ == '__main__':
    main()
