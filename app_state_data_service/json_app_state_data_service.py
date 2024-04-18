import json
import os
from datetime import datetime, timezone, timedelta

from app_state_data_service.app_state_data_service import AppStateDataService
from settings import PRODUCTION


class JSONAppStateDataService(AppStateDataService):
    def __init__(self, data_file='condition_data.json'):
        self.data_file = data_file

    def create_app_state_data(self):
        if not os.path.exists(self.data_file):
            with open(self.data_file, mode='w') as file:
                json.dump({}, file)

    def set_product_data(self, pid: int, last_update: str):
        app_state_data = self._load_app_state_data()
        app_state_data[str(pid)] = last_update
        self._save_app_state_data(app_state_data)

    def get_product_data(self, pid: int) -> str:
        app_state_data = self._load_app_state_data()
        return app_state_data.get(str(pid))

    def update_product_data(self, pid: int, last_update: str):
        app_state_data = self._load_app_state_data()
        app_state_data[str(pid)] = last_update
        self._save_app_state_data(app_state_data)

    @staticmethod
    def create_default_last_update() -> str:
        current_datetime = datetime.now(timezone.utc)
        formatted_datetime = current_datetime.strftime('%Y-%m-%dT%H:%M:%SZ')
        if not PRODUCTION:
            modified_datetime = current_datetime - timedelta(days=4)
            formatted_datetime = modified_datetime.strftime('%Y-%m-%dT%H:%M:%SZ')
        return formatted_datetime

    def _load_app_state_data(self):
        if not os.path.exists(self.data_file):
            self.create_app_state_data()
        with open(self.data_file, mode='r') as file:
            return json.load(file)

    def _save_app_state_data(self, app_state_data):
        with open(self.data_file, mode='w') as file:
            json.dump(app_state_data, file)
