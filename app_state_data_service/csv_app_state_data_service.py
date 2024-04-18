import csv
import os
from datetime import datetime, timezone

from app_state_data_service.app_state_data_service import AppStateDataService


class CSVAppStateDataService(AppStateDataService):
    def __init__(self, data_file='condition_data.csv'):
        self.data_file = data_file

    def create_app_state_data(self):
        if not os.path.exists(self.data_file):
            with open(self.data_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['pid', 'last_update'])

    def set_product_data(self, pid: int, last_update: str):

        if self.get_product_data(pid=pid):
            self.update_product_data(pid=pid, last_update=last_update)
            return

        with open(self.data_file, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([pid, last_update])

    def get_product_data(self, pid: int) -> (str, None):
        try:
            with open(self.data_file, mode='r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == str(pid):
                        return row[1]
        except IndexError:
            return None

    def update_product_data(self, pid: int, last_update: str):
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
    def create_default_last_update() -> str:
        current_datetime = datetime.now(timezone.utc)
        formatted_datetime = current_datetime.strftime('%Y-%m-%dT%H:%M:%SZ')
        return formatted_datetime
