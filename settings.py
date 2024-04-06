from app_state_data_service.json_app_state_data_service import JSONAppStateDataService
from notification_services.telegram_notification_service import TelegramNotificationService

APP_STATE_SERVICE = JSONAppStateDataService

DEFAULT_EXCEL_FILE_PATH = 'product_ids.xlsx'

NOTIFICATION_SERVICES = (TelegramNotificationService, )
