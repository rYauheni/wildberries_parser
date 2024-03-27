from time import sleep

from condition_data import create_condition, set_condition, get_condition, set_default_last_update, update_condition
from parser import get_messages
from parse_excel import extract_ids_from_excel
from telegram_bot import send_message


def main():
    create_condition()
    file_path = 'product_ids_template.xlsx'
    products_ids = extract_ids_from_excel(file_path=file_path)
    # default_last_update = set_default_last_update()
    default_last_update = '2024-03-24T13:06:31Z'
    for pid in products_ids:
        set_condition(pid, default_last_update)

    while True:
        for pid in products_ids:
            messages = get_messages(pid=pid)
            if messages:
                for message in messages:
                    send_message(message=message)

        sleep(600)


if __name__ == '__main__':
    main()
