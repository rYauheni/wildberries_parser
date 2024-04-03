from excel_utils import get_excel_file_path, extract_ids_from_excel
from exceptions.error_messages import FILE_NOT_FOUND_MESSAGE
from exceptions.exceptions import FileError
from notification_services.notification_messages import create_messages_list
from objects.product import Product
from parser import get_product_data
from settings import APP_STATE_SERVICE, NOTIFICATION_SERVICE
# from notification_services.telegram_notification_service import send_message


def main():
    app_state_service = APP_STATE_SERVICE()
    notification_service = NOTIFICATION_SERVICE()
    app_state_service.create_app_state_data()
    file_path = get_excel_file_path()
    try:
        products_ids = extract_ids_from_excel(file_path=file_path)
    except FileError:
        notification_service.send_message(message=FILE_NOT_FOUND_MESSAGE)
        return
    # last_update = app_state_service.set_default_last_update()
    last_update = '2024-03-31T13:06:31Z'
    for pid in products_ids:
        product = Product(id=pid)
        app_state_service.set_app_state_data(pid, last_update)
        product.last_update = app_state_service.get_app_state_data(pid=product.id)
        get_product_data(product=product)
        messages_list = create_messages_list(product=product)

        for message in messages_list:
            notification_service.send_message(message=message)


    # for pid in products_ids:
    #     messages = get_messages(pid=pid, app_state_service=app_state_service)
    #     if messages:
    #         for message in messages:
    #             send_message(message=message)
    # print('====DONE====')


if __name__ == '__main__':
    main()
