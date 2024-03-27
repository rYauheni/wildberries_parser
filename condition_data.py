import csv
from datetime import datetime, timezone


def create_condition():
    with open('condition_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['pid', 'last_update'])


def set_condition(pid: int, last_update: str):
    with open("condition_data.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([pid, last_update])


def get_condition(pid: int) -> (str, None):
    with open('condition_data.csv', mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == str(pid):
                return row[1]


def update_condition(pid: int, last_update: str):

    rows = []
    with open('condition_data.csv', mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == str(pid):
                row[1] = last_update
            rows.append(row)

    with open('condition_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)


def set_default_last_update() -> str:
    current_datetime = datetime.now(timezone.utc)
    formatted_datetime = current_datetime.strftime('%Y-%m-%dT%H:%M:%SZ')
    return str(formatted_datetime)
