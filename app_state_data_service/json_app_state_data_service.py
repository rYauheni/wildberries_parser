import json
import os
from datetime import datetime, timezone, timedelta
from time import time

from app_state_data_service.app_state_data_service import AppStateDataService
from settings import PRODUCTION


class JSONAppStateDataService(AppStateDataService):
    def __init__(self, data_file='condition_data.json'):
        self.data_file = data_file

    def create_app_state_data(self):
        if not os.path.exists(self.data_file):
            with open(self.data_file, mode='w') as file:
                json.dump({}, file)

    def set_product_data(self, pid: int, last_update: float):
        app_state_data = self._load_app_state_data()
        app_state_data[str(pid)] = last_update
        self._save_app_state_data(app_state_data)

    def get_product_data(self, pid: int) -> str:
        app_state_data = self._load_app_state_data()
        return app_state_data.get(str(pid))

    def update_product_data(self, pid: int, last_update: float):
        app_state_data = self._load_app_state_data()
        app_state_data[str(pid)] = last_update
        self._save_app_state_data(app_state_data)

    @staticmethod
    def create_default_last_update() -> float:
        last_update = time()
        if not PRODUCTION:
            last_update = last_update - (4 * 24 * 60 * 60)
        return last_update

    def _load_app_state_data(self):
        if not os.path.exists(self.data_file):
            self.create_app_state_data()
        with open(self.data_file, mode='r') as file:
            return json.load(file)

    def _save_app_state_data(self, app_state_data):
        with open(self.data_file, mode='w') as file:
            json.dump(app_state_data, file)
