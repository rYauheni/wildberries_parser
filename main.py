from time import sleep

from app_state_data import create_app_state_data, set_app_state_data, set_default_last_update
from exceptions.exceptions import FileError
from exceptions.error_messages import FILE_NOT_FOUND_MESSAGE
from parser import get_messages
from excel_utils import get_excel_file_path, extract_ids_from_excel
from telegram_bot import send_message


def main():
    create_app_state_data()
    file_path = get_excel_file_path()
    try:
        products_ids = extract_ids_from_excel(file_path=file_path)
    except FileError:
        send_message(FILE_NOT_FOUND_MESSAGE)
        return
    default_last_update = set_default_last_update()
    # default_last_update = '2024-03-24T13:06:31Z'
    for pid in products_ids:
        set_app_state_data(pid, default_last_update)

    while True:
        for pid in products_ids:
            messages = get_messages(pid=pid)
            if messages:
                for message in messages:
                    send_message(message=message)

        sleep(600)


if __name__ == '__main__':
    main()


# from parse_excel import get_excel_file_path
#
# print(get_excel_file_path())
