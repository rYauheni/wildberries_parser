from time import sleep

from app_state_data.app_state_data_csv import CSVAppStateDataStorage
from exceptions.exceptions import FileError
from exceptions.error_messages import FILE_NOT_FOUND_MESSAGE
from parser import get_messages
from excel_utils import get_excel_file_path, extract_ids_from_excel
from settings import APP_STATE_SERVICE
from telegram_bot import send_message


def main():
    app_state_service = APP_STATE_SERVICE()
    app_state_service.create_app_state_data()
    file_path = get_excel_file_path()
    try:
        products_ids = extract_ids_from_excel(file_path=file_path)
    except FileError:
        send_message(FILE_NOT_FOUND_MESSAGE)
        return
    # last_update = app_state_service.set_default_last_update()
    last_update = '2024-03-30T13:06:31Z'
    for pid in products_ids:
        app_state_service.set_app_state_data(pid, last_update)

    for pid in products_ids:
        messages = get_messages(pid=pid, app_state_service=app_state_service)
        if messages:
            for message in messages:
                send_message(message=message)
    print('====DONE====')


if __name__ == '__main__':
    main()
