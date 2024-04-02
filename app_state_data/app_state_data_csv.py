import csv
from datetime import datetime, timezone

from app_state_data.app_state_data_storage import AppStateDataStorage


class CSVAppStateDataStorage(AppStateDataStorage):
    def __init__(self, data_file='condition_data.csv'):
        self.data_file = data_file

    def create_app_state_data(self):
        with open(self.data_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['pid', 'last_update'])

    def set_app_state_data(self, pid: int, last_update: str):
        with open(self.data_file, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([pid, last_update])

    def get_app_state_data(self, pid: int) -> (str, None):
        with open(self.data_file, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == str(pid):
                    return row[1]
        return None

    def update_app_state_data(self, pid: int, last_update: str):
        rows = []
        with open(self.data_file, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == str(pid):
                    row[1] = last_update
                rows.append(row)

        with open(self.data_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)

    @staticmethod
    def set_default_last_update() -> str:
        current_datetime = datetime.now(timezone.utc)
        formatted_datetime = current_datetime.strftime('%Y-%m-%dT%H:%M:%SZ')
        return formatted_datetime
